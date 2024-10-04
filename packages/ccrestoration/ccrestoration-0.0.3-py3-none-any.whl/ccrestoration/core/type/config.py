from enum import Enum


class ConfigType(str, Enum):
    # RealESRGAN
    RealESRGAN_RealESRGAN_x4plus_4x = "RealESRGAN_RealESRGAN_x4plus_4x.pth"
    RealESRGAN_RealESRGAN_x4plus_anime_6B_4x = "RealESRGAN_RealESRGAN_x4plus_anime_6B_4x.pth"
    RealESRGAN_RealESRGAN_x2plus_2x = "RealESRGAN_RealESRGAN_x2plus_2x.pth"
    RealESRGAN_realesr_animevideov3_4x = "RealESRGAN_realesr_animevideov3_4x.pth"

    RealESRGAN_AnimeJaNai_HD_V3_Compact_2x = "RealESRGAN_AnimeJaNai_HD_V3_Compact_2x.pth"
    RealESRGAN_AniScale_2_Compact_2x = "RealESRGAN_AniScale_2_Compact_2x.pth"
    RealESRGAN_Ani4Kv2_Compact_2x = "RealESRGAN_Ani4Kv2_Compact_2x.pth"

    # RealCUGAN
    RealCUGAN_Conservative_2x = "RealCUGAN_Conservative_2x.pth"
    RealCUGAN_Denoise1x_2x = "RealCUGAN_Denoise1x_2x.pth"
    RealCUGAN_Denoise2x_2x = "RealCUGAN_Denoise2x_2x.pth"
    RealCUGAN_Denoise3x_2x = "RealCUGAN_Denoise3x_2x.pth"
    RealCUGAN_No_Denoise_2x = "RealCUGAN_No_Denoise_2x.pth"
    RealCUGAN_Conservative_3x = "RealCUGAN_Conservative_3x.pth"
    RealCUGAN_Denoise3x_3x = "RealCUGAN_Denoise3x_3x.pth"
    RealCUGAN_No_Denoise_3x = "RealCUGAN_No_Denoise_3x.pth"
    RealCUGAN_Conservative_4x = "RealCUGAN_Conservative_4x.pth"
    RealCUGAN_Denoise3x_4x = "RealCUGAN_Denoise3x_4x.pth"
    RealCUGAN_No_Denoise_4x = "RealCUGAN_No_Denoise_4x.pth"
    RealCUGAN_Pro_Conservative_2x = "RealCUGAN_Pro_Conservative_2x.pth"
    RealCUGAN_Pro_Denoise3x_2x = "RealCUGAN_Pro_Denoise3x_2x.pth"
    RealCUGAN_Pro_No_Denoise_2x = "RealCUGAN_Pro_No_Denoise_2x.pth"
    RealCUGAN_Pro_Conservative_3x = "RealCUGAN_Pro_Conservative_3x.pth"
    RealCUGAN_Pro_Denoise3x_3x = "RealCUGAN_Pro_Denoise3x_3x.pth"
    RealCUGAN_Pro_No_Denoise_3x = "RealCUGAN_Pro_No_Denoise_3x.pth"
