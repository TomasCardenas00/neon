from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"  
AUTH = ("neo4j", "contrasena")

def buscar_residentes(limite=10):
    query = """
    MATCH (r:Residente)-[:ES_PERSONA]->(p:Persona)
    OPTIONAL MATCH (r)-[:OCUPA_CAMA]->(c:Cama)
    OPTIONAL MATCH (e:Empleado)-[:RESPONSABLE_DE]->(r)
    OPTIONAL MATCH (e)-[:ES_PERSONA]->(p_emp:Persona)
    RETURN 
        r.id AS id_residente,
        p.nombre_persona + ' ' + p.apellido_persona AS residente,
        p.numero_documento AS documento,
        r.estado AS estado,
        c.codigo_cama AS cama,
        p_emp.nombre_persona + ' ' + p_emp.apellido_persona AS enfermera_cargo
    LIMIT $limite
    """
    
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        # Verifica que la conexión funcione
        driver.verify_connectivity()
        
        records, summary, keys = driver.execute_query(
            query, 
            limite=limite,
            database_="geriatrico"
        )
        
        print(f"--- MOSTRANDO {len(records)} RESIDENTES ---")
        for record in records:
            print(f"ID: {record['id_residente']}")
            print(f"Nombre: {record['residente']} (Doc: {record['documento']})")
            print(f"Estado: {record['estado']} | Cama: {record['cama']}")
            print(f"Enfermera a cargo: {record['enfermera_cargo']}")
            print("-" * 40)


buscar_residentes(limite=5)