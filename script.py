from adapter import BioCypherAdapter

adapter = BioCypherAdapter(db_name="tum-ai")

adapter.write_to_csv_for_admin_import()