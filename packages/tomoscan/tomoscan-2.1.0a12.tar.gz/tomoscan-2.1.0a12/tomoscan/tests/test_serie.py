# coding: utf-8

import os
import tempfile

import pytest

from tomoscan.esrf.scan.mock import MockNXtomo
from tomoscan.esrf.volume.edfvolume import EDFVolume
from tomoscan.serie import (
    Serie,
    check_serie_is_consistant_frm_sample_name,
    sequences_to_series_from_sample_name,
    serie_is_complete_from_group_size,
)


@pytest.mark.parametrize("use_identifiers", [True, False])
def test_serie_scan(use_identifiers):
    """simple test of a serie"""
    with tempfile.TemporaryDirectory() as dir_:
        serie1 = Serie(use_identifiers=use_identifiers)
        assert isinstance(serie1.name, str)
        serie2 = Serie("test", use_identifiers=use_identifiers)
        assert serie2.name == "test"
        assert len(serie2) == 0
        scan1 = MockNXtomo(dir_, n_proj=2).scan
        scan2 = MockNXtomo(dir_, n_proj=2).scan
        serie3 = Serie("test", [scan1, scan2], use_identifiers=use_identifiers)
        assert serie3.name == "test"
        assert len(serie3) == 2

        with pytest.raises(TypeError):
            serie1.append("toto")

        assert scan1 not in serie1
        serie1.append(scan1)
        assert len(serie1) == 1
        assert scan1 in serie1
        serie1.append(scan1)
        serie1.remove(scan1)
        serie1.name = "toto"
        with pytest.raises(TypeError):
            serie1.name = 12
        with pytest.raises(TypeError):
            serie1.remove(12)
        serie1.append(scan2)
        serie1.append(scan1)
        assert len(serie1) == 3
        serie1.remove(scan1)
        assert len(serie1) == 2
        serie1 == Serie("toto", (scan1, scan2), use_identifiers=use_identifiers)
        assert scan1 in serie1
        assert scan2 in serie1

        identifiers_list = serie1.to_dict_of_str()
        assert type(identifiers_list["objects"]) is list
        assert len(identifiers_list["objects"]) == 2
        for id_str in identifiers_list["objects"]:
            assert isinstance(id_str, str)
        assert serie1 != 12


@pytest.mark.parametrize("use_identifiers", [True, False])
def test_serie_volume(use_identifiers):
    volume_1 = EDFVolume(folder="test")
    volume_2 = EDFVolume()
    volume_3 = EDFVolume(folder="test2")
    volume_4 = EDFVolume()

    serie1 = Serie("Volume serie", [volume_1, volume_2])
    assert volume_1 in serie1
    assert volume_2 in serie1
    assert volume_3 not in serie1
    assert volume_4 not in serie1
    serie1.remove(volume_2)
    serie1.append(volume_3)

    identifiers_list = serie1.to_dict_of_str()
    assert type(identifiers_list["objects"]) is list
    assert len(identifiers_list["objects"]) == 2
    for id_str in identifiers_list["objects"]:
        assert isinstance(id_str, str)

    serie2 = Serie.from_dict_of_str(serie1.to_dict_of_str())
    assert len(serie2) == 2
    with pytest.raises(TypeError):
        Serie.from_dict_of_str({"name": "toto", "objects": (12, 13)})


def test_serie_utils():
    """test utils function from Serie"""
    with tempfile.TemporaryDirectory() as tmp_path:
        dir_1 = os.path.join(tmp_path, "scan1")
        dir_2 = os.path.join(tmp_path, "scan2")
        dir_3 = os.path.join(tmp_path, "scan3")
        for dir_folder in (dir_1, dir_2, dir_3):
            os.makedirs(dir_folder)
        scan_s1_1 = MockNXtomo(dir_1, n_proj=2, sample_name="toto").scan
        scan_s1_2 = MockNXtomo(dir_2, n_proj=2, sample_name="toto").scan
        scan_s2_2 = MockNXtomo(dir_3, n_proj=2, sample_name="titi").scan

        found_series = sequences_to_series_from_sample_name(
            (scan_s1_1, scan_s1_2, scan_s2_2)
        )
        assert len(found_series) == 2
        with pytest.raises(TypeError):
            sequences_to_series_from_sample_name([12])
        for serie in found_series:
            check_serie_is_consistant_frm_sample_name(serie)

        with pytest.raises(ValueError):
            check_serie_is_consistant_frm_sample_name(
                Serie("test", [scan_s1_1, scan_s2_2])
            )

        dir_4 = os.path.join(tmp_path, "scan4")
        dir_5 = os.path.join(tmp_path, "scan5")
        scan_zserie_1 = MockNXtomo(
            dir_4, n_proj=2, sample_name="z-serie", group_size=2
        ).scan
        scan_zserie_2 = MockNXtomo(
            dir_5, n_proj=2, sample_name="z-serie", group_size=2
        ).scan
        assert not serie_is_complete_from_group_size(
            [
                scan_zserie_1,
            ]
        )
        assert serie_is_complete_from_group_size([scan_zserie_1, scan_zserie_2])

        dir_6 = os.path.join(tmp_path, "scan6")
        scan_zserie_3 = MockNXtomo(
            dir_6, n_proj=2, sample_name="z-serie", group_size=2
        ).scan
        assert serie_is_complete_from_group_size(
            [scan_zserie_1, scan_zserie_2, scan_zserie_3]
        )

        with pytest.raises(TypeError):
            serie_is_complete_from_group_size([1, 2])
