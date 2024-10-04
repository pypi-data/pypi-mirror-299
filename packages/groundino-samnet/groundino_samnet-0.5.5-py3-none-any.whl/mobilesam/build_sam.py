# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch

from functools import partial

from .modeling import ImageEncoderViT, MaskDecoder, PromptEncoder, Sam, TwoWayTransformer, TinyViT




def build_mobile_sam(checkpoint=None):
    """Builds and returns a Mobile Segment Anything Model (Mobile-SAM) for efficient image segmentation."""
    return _build_sam(
        encoder_embed_dim=[64, 128, 160, 320],
        encoder_depth=[2, 2, 6, 2],
        encoder_num_heads=[2, 4, 5, 10],
        encoder_global_attn_indexes=None,
        mobile_sam=True,
        checkpoint=checkpoint,
    )

sam_model_registry_mobile = {
    "mobilesam": build_mobile_sam
}


def _build_sam(
    encoder_embed_dim,
    encoder_depth,
    encoder_num_heads,
    encoder_global_attn_indexes,
    checkpoint=None,
    mobile_sam=False,
):
    """
    Builds a Segment Anything Model (SAM) with specified encoder parameters.

    Args:
        encoder_embed_dim (int | List[int]): Embedding dimension for the encoder.
        encoder_depth (int | List[int]): Depth of the encoder.
        encoder_num_heads (int | List[int]): Number of attention heads in the encoder.
        encoder_global_attn_indexes (List[int] | None): Indexes for global attention in the encoder.
        checkpoint (str | None): Path to the model checkpoint file.
        mobile_sam (bool): Whether to build a Mobile-SAM model.

    Returns:
        (SAMModel): A Segment Anything Model instance with the specified architecture.

    Examples:
        >>> sam = _build_sam(768, 12, 12, [2, 5, 8, 11])
        >>> sam = _build_sam([64, 128, 160, 320], [2, 2, 6, 2], [2, 4, 5, 10], None, mobile_sam=True)
    """
    prompt_embed_dim = 256
    image_size = 1024
    vit_patch_size = 16
    image_embedding_size = image_size // vit_patch_size
    image_encoder = (
        TinyViT(
            img_size=1024,
            in_chans=3,
            num_classes=1000,
            embed_dims=encoder_embed_dim,
            depths=encoder_depth,
            num_heads=encoder_num_heads,
            window_sizes=[7, 7, 14, 7],
            mlp_ratio=4.0,
            drop_rate=0.0,
            drop_path_rate=0.0,
            use_checkpoint=False,
            mbconv_expand_ratio=4.0,
            local_conv_size=3,
            layer_lr_decay=0.8,
        )
    )
    sam = Sam(
        image_encoder=image_encoder,
        prompt_encoder=PromptEncoder(
            embed_dim=prompt_embed_dim,
            image_embedding_size=(image_embedding_size, image_embedding_size),
            input_image_size=(image_size, image_size),
            mask_in_chans=16,
        ),
        mask_decoder=MaskDecoder(
            num_multimask_outputs=3,
            transformer=TwoWayTransformer(
                depth=2,
                embedding_dim=prompt_embed_dim,
                mlp_dim=2048,
                num_heads=8,
            ),
            transformer_dim=prompt_embed_dim,
            iou_head_depth=3,
            iou_head_hidden_dim=256,
        ),
        pixel_mean=[123.675, 116.28, 103.53],
        pixel_std=[58.395, 57.12, 57.375],
    )
    if checkpoint is not None:
        state_dict = torch.load(checkpoint)
        sam.load_state_dict(state_dict)
    sam.eval()
    return sam

def build_sam(ckpt="sam_b.pt"):
    """
    Builds and returns a Segment Anything Model (SAM) based on the provided checkpoint.

    Args:
        ckpt (str | Path): Path to the checkpoint file or name of a pre-defined SAM model.

    Returns:
        (SAMModel | SAM2Model): A configured and initialized SAM or SAM2 model instance.

    Raises:
        FileNotFoundError: If the provided checkpoint is not a supported SAM model.

    Examples:
        >>> sam_model = build_sam("sam_b.pt")
        >>> sam_model = build_sam("path/to/custom_checkpoint.pt")

    Notes:
        Supported pre-defined models include:
        - SAM: 'sam_h.pt', 'sam_l.pt', 'sam_b.pt', 'mobile_sam.pt'
        - SAM2: 'sam2_t.pt', 'sam2_s.pt', 'sam2_b.pt', 'sam2_l.pt'
    """
    model_builder = None
    ckpt = str(ckpt)  # to allow Path ckpt types
    for k in sam_model_map.keys():
        if ckpt.endswith(k):
            model_builder = sam_model_map.get(k)

    if not model_builder:
        raise FileNotFoundError(f"{ckpt} is not a supported SAM model. Available models are: \n {sam_model_map.keys()}")

    return model_builder(ckpt)


