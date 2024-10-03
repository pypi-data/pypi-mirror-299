from niklibrary.helper.Cmd import Cmd


class Overlay:

    def __init__(self, overlay_path):
        self.path = overlay_path

    def extract_overlay(self, extract_dir_path):
        cmd = Cmd()
        if cmd.decompile_apk(self.path, extract_dir_path):
            return True
        return False
