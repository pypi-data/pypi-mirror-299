from niklibrary.helper.Cmd import Cmd


class Overlay:

    def __init__(self, overlay_path):
        self.path = overlay_path

    def extract_overlay(self, extract_dir_path=None):
        cmd = Cmd()
        if extract_dir_path is None:
            extract_dir_path = str(self.path).replace(".apk","") + "_extracted"
        if cmd.decompile_apk(self.path, extract_dir_path):
            return True
        return False
