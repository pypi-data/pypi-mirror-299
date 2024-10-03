from niklibrary.helper.F import F
from niklibrary.helper.Statics import Statics
from niklibrary.oem.GoogleOem import GoogleOem


class ExtractOp:

    @staticmethod
    def extract_overlays(android_version, oem, oem_overlays_directory):
        match oem:
            case 'cheetah' | 'husky':
                oem_overlays_dir = f"{oem_overlays_directory}{Statics.dir_sep}{android_version}{Statics.dir_sep}{oem}"
                F.make_dir(oem_overlays_dir)
                c = GoogleOem(android_version=android_version, oem=oem)
                c.extract_overlay(oem_overlays_dir)
            case _:
                print("default")