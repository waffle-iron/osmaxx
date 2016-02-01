import os
from unittest import TestCase, mock

from django.conf import settings

from converters.gis_converter.bootstrap import bootstrap


class BootStrapperTest(TestCase):
    def test_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(pbf_file_path=settings.OSMAXX_CONVERSION_SERVICE['PBF_PLANET_FILE_PATH'])
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            bootstrapper._filter_data()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/filter/drop_and_recreate/drop_and_recreate.sql',
                'sql/filter/address/000_setup-drop_and_recreate_table.sql',
                'sql/filter/address/010_address.sql',
                'sql/filter/address/020_entrance.sql',
                'sql/filter/address/030_interpolation.sql',
                'sql/filter/adminarea_boundary/000_setup-drop_and_recreate_table_adminarea.sql',
                'sql/filter/adminarea_boundary/010_adminarea.sql',
                'sql/filter/adminarea_boundary/020_setup-drop_and_recreate_table_boundary.sql',
                'sql/filter/adminarea_boundary/030_boundary.sql',
                'sql/filter/building/000_setup-drop_and_recreate_table_building.sql',
                'sql/filter/building/010_building.sql',
                'sql/filter/landuse/000_setup-drop_and_recreate_table_landuse.sql',
                'sql/filter/landuse/010_landuse.sql',
                'sql/filter/military/000_setup-drop_and_recreate_table_military_a.sql',
                'sql/filter/military/010_military_a.sql',
                'sql/filter/military/020_setup-drop_and_recreate_table_military_p.sql',
                'sql/filter/military/030_military_p.sql',
                'sql/filter/natural/natural.sql',
                'sql/filter/nonop/nonop.sql',
                'sql/filter/geoname/000_setup-geoname_table.sql',
                'sql/filter/geoname/010_geoname_l.sql',
                'sql/filter/geoname/020_geoname_p.sql',
                'sql/filter/pow/pow.sql',
                'sql/filter/poi/poi.sql',
                'sql/filter/misc/000_setup_misc_table.sql',
                'sql/filter/misc/010_barrier.sql',
                'sql/filter/misc/020_natural.sql',
                'sql/filter/misc/030_traffic_calming.sql',
                'sql/filter/misc/040_air_traffic.sql',
                'sql/filter/transport/transport.sql',
                'sql/filter/railway/railway.sql',
                'sql/filter/road/road.sql',
                'sql/filter/route/route.sql',
                'sql/filter/traffic/traffic.sql',
                'sql/filter/utility/utility.sql',
                'sql/filter/water/water.sql',
                'sql/filter/create_view/000_create_view.sql',
            ]
            expected_calls = [
                mock.call(
                    os.path.join(
                        base_path_to_bootstrap,
                        relative_script_path
                    )
                ) for relative_script_path in expected_script_order
            ]
            self.assertListEqual(expected_calls, postgres_mock.execute_sql_file.mock_calls)

    def test_function_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(pbf_file_path=settings.OSMAXX_CONVERSION_SERVICE['PBF_PLANET_FILE_PATH'])
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            bootstrapper._setup_db_functions()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/functions/0010_cast_to_positive_integer.sql',
                'sql/functions/0020_building_height.sql',
                'sql/functions/0030_transliterate.sql',
                'sql/functions/0040_interpolate_addresses.sql',
                'sql/functions/0050_cast_to_int.sql',
            ]
            expected_calls = [
                mock.call(
                    os.path.join(
                        base_path_to_bootstrap,
                        relative_script_path
                    )
                ) for relative_script_path in expected_script_order
            ]
            self.assertListEqual(expected_calls, postgres_mock.execute_sql_file.mock_calls)
