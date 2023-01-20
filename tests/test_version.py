import itertools
import operator

import pretend
import pytest
from packaging.version import Version

from packaging_legacy.version import LegacyVersion, parse


@pytest.mark.parametrize(
    ("version", "klass"), [("1.0", Version), ("1-1-1", LegacyVersion)]
)
def test_parse(version, klass):
    assert isinstance(parse(version), klass)


class TestVersion:
    def test_compare_legacyversion_version(self):
        result = sorted([Version("0"), LegacyVersion("1")])
        assert result == [LegacyVersion("1"), Version("0")]


VERSIONS = [
    # Implicit epoch of 0
    "1.0.dev456",
    "1.0a1",
    "1.0a2.dev456",
    "1.0a12.dev456",
    "1.0a12",
    "1.0b1.dev456",
    "1.0b2",
    "1.0b2.post345.dev456",
    "1.0b2.post345",
    "1.0b2-346",
    "1.0c1.dev456",
    "1.0c1",
    "1.0rc2",
    "1.0c3",
    "1.0",
    "1.0.post456.dev34",
    "1.0.post456",
    "1.1.dev1",
    "1.2+123abc",
    "1.2+123abc456",
    "1.2+abc",
    "1.2+abc123",
    "1.2+abc123def",
    "1.2+1234.abc",
    "1.2+123456",
    "1.2.r32+123456",
    "1.2.rev33+123456",
    # Explicit epoch of 1
    "1!1.0.dev456",
    "1!1.0a1",
    "1!1.0a2.dev456",
    "1!1.0a12.dev456",
    "1!1.0a12",
    "1!1.0b1.dev456",
    "1!1.0b2",
    "1!1.0b2.post345.dev456",
    "1!1.0b2.post345",
    "1!1.0b2-346",
    "1!1.0c1.dev456",
    "1!1.0c1",
    "1!1.0rc2",
    "1!1.0c3",
    "1!1.0",
    "1!1.0.post456.dev34",
    "1!1.0.post456",
    "1!1.1.dev1",
    "1!1.2+123abc",
    "1!1.2+123abc456",
    "1!1.2+abc",
    "1!1.2+abc123",
    "1!1.2+abc123def",
    "1!1.2+1234.abc",
    "1!1.2+123456",
    "1!1.2.r32+123456",
    "1!1.2.rev33+123456",
]
LEGACY_VERSIONS = ["foobar", "a cat is fine too", "lolwut", "1-0", "2.0-a1"]


class TestLegacyVersion:
    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_valid_legacy_versions(self, version):
        LegacyVersion(version)

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_str_repr(self, version):
        assert str(LegacyVersion(version)) == version
        assert repr(LegacyVersion(version)) == "<LegacyVersion({})>".format(
            repr(version)
        )

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_hash(self, version):
        assert hash(LegacyVersion(version)) == hash(LegacyVersion(version))

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_public(self, version):
        assert LegacyVersion(version).public == version

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_base_version(self, version):
        assert LegacyVersion(version).base_version == version

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_epoch(self, version):
        assert LegacyVersion(version).epoch == -1

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_release(self, version):
        assert LegacyVersion(version).release is None

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_local(self, version):
        assert LegacyVersion(version).local is None

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_pre(self, version):
        assert LegacyVersion(version).pre is None

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_is_prerelease(self, version):
        assert not LegacyVersion(version).is_prerelease

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_dev(self, version):
        assert LegacyVersion(version).dev is None

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_is_devrelease(self, version):
        assert not LegacyVersion(version).is_devrelease

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_post(self, version):
        assert LegacyVersion(version).post is None

    @pytest.mark.parametrize("version", VERSIONS + LEGACY_VERSIONS)
    def test_legacy_version_is_postrelease(self, version):
        assert not LegacyVersion(version).is_postrelease

    @pytest.mark.parametrize(
        ("left", "right", "op"),
        # Below we'll generate every possible combination of
        # VERSIONS + LEGACY_VERSIONS that should be True for the given operator
        itertools.chain(
            *
            # Verify that the equal (==) operator works correctly
            [[(x, x, operator.eq) for x in VERSIONS + LEGACY_VERSIONS]]
            +
            # Verify that the not equal (!=) operator works correctly
            [
                [
                    (x, y, operator.ne)
                    for j, y in enumerate(VERSIONS + LEGACY_VERSIONS)
                    if i != j
                ]
                for i, x in enumerate(VERSIONS + LEGACY_VERSIONS)
            ]
        ),
    )
    def test_comparison_true(self, left, right, op):
        assert op(LegacyVersion(left), LegacyVersion(right))

    @pytest.mark.parametrize(
        ("left", "right", "op"),
        # Below we'll generate every possible combination of
        # VERSIONS + LEGACY_VERSIONS that should be False for the given
        # operator
        itertools.chain(
            *
            # Verify that the equal (==) operator works correctly
            [
                [
                    (x, y, operator.eq)
                    for j, y in enumerate(VERSIONS + LEGACY_VERSIONS)
                    if i != j
                ]
                for i, x in enumerate(VERSIONS + LEGACY_VERSIONS)
            ]
            +
            # Verify that the not equal (!=) operator works correctly
            [[(x, x, operator.ne) for x in VERSIONS + LEGACY_VERSIONS]]
        ),
    )
    def test_comparison_false(self, left, right, op):
        assert not op(LegacyVersion(left), LegacyVersion(right))

    @pytest.mark.parametrize("op", ["lt", "le", "eq", "ge", "gt", "ne"])
    def test_dunder_op_returns_notimplemented(self, op):
        method = getattr(LegacyVersion, f"__{op}__")
        assert method(LegacyVersion("1"), 1) is NotImplemented

    @pytest.mark.parametrize(("op", "expected"), [("eq", False), ("ne", True)])
    def test_compare_other(self, op, expected):
        other = pretend.stub(**{f"__{op}__": lambda other: NotImplemented})

        assert getattr(operator, op)(LegacyVersion("1"), other) is expected
