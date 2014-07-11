from django.test import TestCase
from django.template.loader import find_template_loader

from template_graph.line_stream import get_template_loaders_dirs


class TemplateLoadersDirsTestCase(TestCase):

    def test_get_template_loaders(self):
        tloaders, tdirs = get_template_loaders_dirs()
        fs_loader = find_template_loader('django.template.loaders.filesystem.Loader')
        app_loader = find_template_loader('django.template.loaders.app_directories.Loader')
        self.assertEqual(tloaders[0].__class__, fs_loader.__class__)
        self.assertEqual(tloaders[1].__class__, app_loader.__class__)
