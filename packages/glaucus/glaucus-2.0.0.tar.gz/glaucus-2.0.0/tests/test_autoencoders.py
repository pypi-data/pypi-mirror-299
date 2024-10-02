# Copyright 2024 The Aerospace Corporation
# This file is a part of Glaucus
# SPDX-License-Identifier: LGPL-3.0-or-later

"""ensure autoencoders are working"""

import unittest

import torch
from hypothesis import given, settings
from hypothesis import strategies as st

from glaucus import FullyConnectedAE, GlaucusAE, GlaucusRVQVAE, GlaucusVAE


class TestAE(unittest.TestCase):
    @given(
        data_format=st.sampled_from(["ncl", "nl"]),
        length=st.integers(min_value=128, max_value=65536),
    )
    @settings(deadline=None, max_examples=10)
    def test_vqvae_roundtrip(self, data_format, length):
        """the  output size should always be the same as the input size"""
        if data_format == "ncl":
            trash_x = torch.randn(1, 2, length, dtype=torch.float32)
        else:
            trash_x = torch.randn(1, length, dtype=torch.complex64)
        ae = GlaucusRVQVAE(data_format=data_format)
        ae.freeze()
        trash_y = ae(trash_x)
        self.assertEqual(trash_x.shape, trash_y.shape)

    def test_ae_roundtrip(self):
        """the  output size should always be the same as the input size"""
        for AE in [GlaucusAE, FullyConnectedAE, GlaucusVAE]:
            for data_format in ["ncl", "nl"]:
                for domain in ["time", "freq"]:
                    # note if we use a diff spatial_size, will need to gen new encoder & decoder bocks
                    spatial_size = 4096
                    if data_format == "ncl":
                        trash_x = torch.randn(7, 2, spatial_size)
                    else:
                        trash_x = torch.randn(7, spatial_size, dtype=torch.complex64)
                    ae = AE(domain=domain, data_format=data_format)
                    trash_y = ae(trash_x)[0]
                    self.assertEqual(trash_x.shape, trash_y.shape)

    def test_ae_quantization(self):
        """If quantization enabled, should use quint8 as latent output"""
        for AE in [FullyConnectedAE, GlaucusAE, GlaucusVAE]:
            for data_format in ["ncl", "nl"]:
                for is_quantized in [True, False]:
                    target = torch.quint8 if is_quantized else torch.float32
                    # note if we use a diff spatial_size, will need to gen new encoder & decoder bocks
                    spatial_size = 4096
                    if data_format == "ncl":
                        trash_x = torch.randn(7, 2, spatial_size)
                    else:
                        trash_x = torch.randn(7, spatial_size, dtype=torch.complex64)
                    ae = AE(bottleneck_quantize=is_quantized, data_format=data_format)
                    if is_quantized:
                        # this will prepare the quant/dequant layers
                        torch.quantization.prepare(ae, inplace=True)
                        # this applies the quantization coefficients within the bottleneck
                        torch.quantization.convert(ae.cpu(), inplace=True)
                    trash_latent = ae(trash_x)[1]
                    self.assertEqual(trash_latent.dtype, target)

    def test_ae_backprop(self):
        """catch errors during backpropagation"""
        for data_format in ["ncl", "nl"]:
            for AE in [FullyConnectedAE, GlaucusAE, GlaucusVAE]:
                for is_quantized in [True, False]:
                    # note if we use a diff spatial_size, will need to gen new encoder & decoder bocks
                    spatial_size = 4096
                    if data_format == "ncl":
                        trash_x = torch.randn(7, 2, spatial_size)
                    else:
                        trash_x = torch.randn(7, spatial_size, dtype=torch.complex64)
                    ae = AE(bottleneck_quantize=is_quantized, data_format=data_format)
                    if is_quantized:
                        # this will prepare the quant/dequant layers
                        torch.quantization.prepare(ae, inplace=True)
                        # this applies the quantization coefficients within the bottleneck
                        torch.quantization.convert(ae.cpu(), inplace=True)
                    loss, _ = ae.step((trash_x, None), 0)
                    # will raise RuntimeError here if there is an issue with backprop
                    loss.backward()
