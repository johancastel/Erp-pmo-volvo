# src/services/validation_service.py
import pandas as pd

class ValidationService:
    @staticmethod
    def validate_float(value):
        """
        Validates if a string value represents a valid real number.
        Converts commas to periods before validation.
        """
        if not value:
            return False
        clean_val = str(value).replace(',', '.').strip()
        try:
            float(clean_val)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_checklist_filled(df_master, movil_id):
        """
        Checks if the entire checklist (levels, mechanical, electrical, and activities)
        is completely and correctly filled for a specific vehicle (movil_id).
        """
        # Filter master rows for this vehicle that haven't been finalized yet (Técnico is empty/blank)
        vehicle_rows = df_master[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == '')
        ]
        if vehicle_rows.empty:
            return True
            
        first_row = vehicle_rows.iloc[0]
        tipo_nov = first_row.get('Tipo Novedad', 'ALISTAMIENTO')
        if tipo_nov in ['CORRECTIVO', 'PREVENTIVO']:
            for idx, row in vehicle_rows.iterrows():
                det_mec = str(row.get('Detalles / Novedades', '')).strip()
                obs_mec = str(row.get('Observaciones', '')).strip()
                if det_mec == "" or obs_mec == "":
                    return False
            return True
        
        # 1. Validate main checklist selection columns
        first_row = vehicle_rows.iloc[0]
        checklist_cols = [
            'Nivel Aceite Motor (SI/NO)', 'Nivel Refrigerante (SI/NO)', 
            'Nivel Aceite Hidráulico (SI/NO)', 'Nivel Limpiabrisas (SI/NO)',
            'Inspección Ducto Admisión', 'Drenar Tanques',
            'Revisión de Fugas', 'Separador de Humedad', 'Inspección Embrague', 
            'Inspección Palanca', 'Inspección Ventilador', 'Inspección Suspensión', 
            'Inspección Frenos', 'Inspección Dirección',
            'Elec. Luces', 'Elec. Tablero', 'Elec. Rutero', 
            'Elec. Arranque', 'Elec. Puertas', 'Elec. Baterías'
        ]
        for col in checklist_cols:
            val = str(first_row.get(col, '')).strip()
            if val == "":
                return False
                
        # Validate that if level response was SI, the corresponding liters entry is a valid number
        level_pairs = [
            ('Nivel Aceite Motor (SI/NO)', 'Nivel Aceite Motor (L)'),
            ('Nivel Refrigerante (SI/NO)', 'Nivel Refrigerante (L)'),
            ('Nivel Aceite Hidráulico (SI/NO)', 'Nivel Aceite Hidráulico (L)'),
            ('Nivel Limpiabrisas (SI/NO)', 'Nivel Limpiabrisas (L)'),
        ]
        for si_no_col, cant_col in level_pairs:
            si_no_val = str(first_row.get(si_no_col, '')).strip()
            cant_val = str(first_row.get(cant_col, '')).strip()
            if si_no_val == "SI":
                if not ValidationService.validate_float(cant_val):
                    return False

        # 2. Validate details and observations for every row of this vehicle
        for idx, row in vehicle_rows.reset_index(drop=True).iterrows():
            obs_niv = str(row.get('Observaciones Niveles', '')).strip()
            det_mec = str(row.get('Detalles / Novedades', '')).strip()
            obs_mec = str(row.get('Observaciones', '')).strip()
            det_elec = str(row.get('Detalles Eléctrico', '')).strip()
            obs_elec = str(row.get('Observaciones Eléctrico', '')).strip()
            
            # The first row of the vehicle requires all three observation sections to be filled
            if idx == 0:
                if obs_niv == "":
                    return False
                if det_mec == "" or obs_mec == "":
                    return False
                if det_elec == "" or obs_elec == "":
                    return False
            else:
                # Additional activity rows must be completely filled if any of their details/obs are initiated
                if (det_mec != "" or obs_mec != "") and (det_mec == "" or obs_mec == ""):
                    return False
                if (det_elec != "" or obs_elec != "") and (det_elec == "" or obs_elec == ""):
                    return False
                
        return True
