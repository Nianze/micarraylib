from micarraylib.datasets import tau2021sse_nigens_loader
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
import numpy as np
import soundata
import pytest
import librosa


def test_tau2021sse_nigens_init():

    a = tau2021sse_nigens_loader.tau2021sse_nigens(download=False, data_home="~/")
    assert a.name == "tau2021sse_nigens"
    assert a.fs == 24000
    assert len(a.array_format) == 1
    assert a.array_format["Eigenmike"] == "A"
    assert len(a.capsule_coords["Eigenmike"]) == 4
    assert list(a.capsule_coords["Eigenmike"].keys()) == ["6", "10", "22", "26"]
    b = _polar2cart(a.capsule_coords["Eigenmike"], "radians")
    # TODO: analize why the atol is needed
    assert np.allclose(
        np.mean(np.array([c for c in b.values()]), axis=0), [0, 0, 0], atol=1e-4
    )
    assert (
        len(a.micarray_clip_ids["Eigenmike"])
        == len(soundata.initialize("tau2021sse_nigens", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B
    assert (
        len(a.clips_list)
        == len(soundata.initialize("tau2021sse_nigens", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B


def test_tau2021sse_nigens_get_audio_numpy():

    a = tau2021sse_nigens_loader.tau2021sse_nigens(
        download=False, data_home="tests/resources/datasets/tau2021sse_nigens"
    )
    A = a.get_audio_numpy("dev/dev-train/fold1_room1_mix001")
    B = a.get_audio_numpy("dev/dev-train/fold1_room1_mix001", fmt="B")

    Al = librosa.load(
        "tests/resources/datasets/tau2021sse_nigens/mic_dev/dev-train/fold1_room1_mix001.wav",
        sr=24000,
        mono=False,
    )[0]
    Bl = librosa.load(
        "tests/resources/datasets/tau2021sse_nigens/foa_dev/dev-train/fold1_room1_mix001.wav",
        sr=24000,
        mono=False,
    )[0]

    assert (B == Bl).all()
    assert (A == Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "b")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenmike")


def test_tau2021sse_nigens_get_audio_events():

    a = tau2021sse_nigens_loader.tau2021sse_nigens(
        download=False, data_home="tests/resources/datasets/tau2021sse_nigens"
    )
    A = a.get_audio_events("dev/dev-train/fold1_room1_mix001")

    with pytest.raises(ValueError):
        a.get_audio_events("a")
