"""Tests for the Vehicle and VehicleCrew models."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Character, Citation, Trivia, Vehicle, VehicleCrew


class TestVehicle:
    def test_table_definition(self):
        table = Vehicle.__table__
        assert table.name == "vehicles"
        assert table.c.vehicle_name.nullable is False
        for column in (
            "vehicle_type",
            "description",
            "parody_of",
            "image_url",
            "source_url",
            "last_updated",
        ):
            assert table.c[column].nullable is True, column
        assert "idx_vehicles_name" in {index.name for index in table.indexes}

    def test_persists_and_reads_back(self, session):
        session.add(
            Vehicle(
                vehicle_name="Spaceball One",
                vehicle_type="Star cruiser",
                parody_of="Star Destroyer (Star Wars)",
            )
        )
        session.commit()

        vehicle = session.scalar(select(Vehicle))
        assert vehicle.vehicle_name == "Spaceball One"
        assert vehicle.parody_of == "Star Destroyer (Star Wars)"

    def test_vehicle_name_is_required(self, session):
        session.add(Vehicle())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_collections_start_empty(self, vehicle):
        assert vehicle.crew == []
        assert vehicle.trivia == []
        assert vehicle.citations == []

    def test_trivia_and_citations_attach_by_vehicle_id(self, session, vehicle):
        session.add_all(
            [
                Trivia(trivia_text="a note", vehicle_id=vehicle.id),
                Citation(
                    citation_number=1, source_text="Spaceballs", vehicle_id=vehicle.id
                ),
            ]
        )
        session.commit()
        assert len(vehicle.trivia) == 1
        assert len(vehicle.citations) == 1

    def test_delete_cascades_crew_and_annotations(self, session, vehicle, character):
        """Regression: deleting a vehicle must let the database cascade."""
        session.add_all(
            [
                VehicleCrew(vehicle_id=vehicle.id, character_id=character.id),
                Trivia(trivia_text="a note", vehicle_id=vehicle.id),
                Citation(
                    citation_number=1, source_text="Spaceballs", vehicle_id=vehicle.id
                ),
            ]
        )
        session.commit()

        session.delete(vehicle)
        session.commit()

        assert session.scalars(select(VehicleCrew)).all() == []
        assert session.scalars(select(Trivia)).all() == []
        assert session.scalars(select(Citation)).all() == []
        assert session.get(Character, character.id) is not None


class TestVehicleCrew:
    def test_table_definition(self):
        table = VehicleCrew.__table__
        assert table.name == "vehicle_crew"
        assert [c.name for c in table.primary_key.columns] == [
            "vehicle_id",
            "character_id",
        ]
        assert table.c.crew_role.nullable is True
        assert "idx_vehicle_crew_character_id" in {i.name for i in table.indexes}

    def test_persists_and_reads_back(self, session, vehicle, character):
        session.add(
            VehicleCrew(
                vehicle_id=vehicle.id, character_id=character.id, crew_role="Captain"
            )
        )
        session.commit()

        crew = session.get(VehicleCrew, (vehicle.id, character.id))
        assert crew.crew_role == "Captain"

    def test_crew_role_is_optional(self, session, vehicle, character):
        session.add(VehicleCrew(vehicle_id=vehicle.id, character_id=character.id))
        session.commit()
        assert session.get(VehicleCrew, (vehicle.id, character.id)).crew_role is None

    def test_character_can_only_be_aboard_a_vehicle_once(
        self, session, vehicle, character
    ):
        session.add(VehicleCrew(vehicle_id=vehicle.id, character_id=character.id))
        session.commit()
        session.add(VehicleCrew(vehicle_id=vehicle.id, character_id=character.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_requires_existing_vehicle_and_character(self, session, vehicle):
        session.add(VehicleCrew(vehicle_id=vehicle.id, character_id=9999))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_relationships_resolve_both_sides(self, session, vehicle, character):
        crew = VehicleCrew(vehicle=vehicle, character=character, crew_role="Co-pilot")
        session.add(crew)
        session.commit()

        assert crew.vehicle is vehicle
        assert crew.character is character
        assert vehicle.crew == [crew]
        assert character.crew_roles == [crew]

    def test_deleting_character_removes_crew_row(self, session, vehicle, character):
        session.add(VehicleCrew(vehicle_id=vehicle.id, character_id=character.id))
        session.commit()

        session.delete(character)
        session.commit()

        assert session.scalars(select(VehicleCrew)).all() == []
        assert session.get(Vehicle, vehicle.id) is not None
