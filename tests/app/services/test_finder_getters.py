#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from unittest.mock import MagicMock, patch

from machine_tools.app.services.finder_getters import (
    get_finder_with_dict_info,
    get_finder_with_dict_names,
    get_finder_with_indexed_info,
    get_finder_with_indexed_names,
    get_finder_with_list_info,
    get_finder_with_list_names,
)


class TestFinderGetters(unittest.TestCase):
    """Тесты для функций получения finder'ов"""

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_01_get_finder_with_list_names(self, mock_container):
        """Тест получения finder'а со списком имен"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_list_names.return_value = mock_finder

        result = get_finder_with_list_names()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_list_names.assert_called_once()

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_02_get_finder_with_list_info(self, mock_container):
        """Тест получения finder'а со списком информации"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_list_info.return_value = mock_finder

        result = get_finder_with_list_info()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_list_info.assert_called_once()

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_03_get_finder_with_dict_names(self, mock_container):
        """Тест получения finder'а со словарем имен"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_dict_names.return_value = mock_finder

        result = get_finder_with_dict_names()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_dict_names.assert_called_once()

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_04_get_finder_with_dict_info(self, mock_container):
        """Тест получения finder'а со словарем информации"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_dict_info.return_value = mock_finder

        result = get_finder_with_dict_info()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_dict_info.assert_called_once()

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_05_get_finder_with_indexed_names(self, mock_container):
        """Тест получения finder'а с индексированными именами"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_indexed_names.return_value = mock_finder

        result = get_finder_with_indexed_names()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_indexed_names.assert_called_once()

    @patch('machine_tools.app.services.finder_getters.FinderContainer')
    def test_06_get_finder_with_indexed_info(self, mock_container):
        """Тест получения finder'а с индексированной информацией"""

        mock_finder = MagicMock()
        mock_container.return_value.finder_with_indexed_info.return_value = mock_finder

        result = get_finder_with_indexed_info()

        self.assertEqual(result, mock_finder)
        mock_container.return_value.finder_with_indexed_info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
