from neo4j import GraphDatabase

# Neo4j'e bağlantı
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

# Veritabanına sorgu gönderme fonksiyonu
def run_query(query):
    with driver.session() as session:
        return session.run(query)

# İlçeler, kategoriler ve diğer bilgileri veritabanına eklemek için sorgular
query = """
// Şehir düğümü
MERGE (ankara:City {name: "Ankara"})

// Kategoriler
MERGE (ilceler:Category {name: "İlçeler"})
MERGE (nufus:Category {name: "Nüfus"})
MERGE (yemekler:Category {name: "Yemekler"})
MERGE (turistikYerler:Category {name: "Turistik Yerler"})

// Şehir ile kategoriler arasında ilişkiler
MERGE (ankara)-[:HAS_CATEGORY]->(ilceler)
MERGE (ankara)-[:HAS_CATEGORY]->(nufus)
MERGE (ankara)-[:HAS_CATEGORY]->(yemekler)
MERGE (ankara)-[:HAS_CATEGORY]->(turistikYerler)

// İlçeler kategorisine ilçe düğümleri ekleme
MERGE (cankaya:District {name: "Çankaya"})
MERGE (kecioren:District {name: "Keçiören"})
MERGE (mamak:District {name: "Mamak"})
MERGE (sincan:District {name: "Sincan"})
MERGE (pursaklar:District {name: "Pursaklar"})
MERGE (ilceler)-[:CONTAINS]->(cankaya)
MERGE (ilceler)-[:CONTAINS]->(kecioren)
MERGE (ilceler)-[:CONTAINS]->(mamak)
MERGE (ilceler)-[:CONTAINS]->(sincan)
MERGE (ilceler)-[:CONTAINS]->(pursaklar)

// Nüfus bilgisi ekleme
MERGE (ankaraNufus:Information {detail: "Ankara'nın nüfusu 5.5 milyon"})
MERGE (cankayaNufus:Information {detail: "Çankaya'nın nüfusu 925 bin"})
MERGE (keciorenNufus:Information {detail: "Keçiören'in nüfusu 940 bin"})
MERGE (mamakNufus:Information {detail: "Mamak'ın nüfusu 660 bin"})
MERGE (nufus)-[:HAS_INFORMATION]->(ankaraNufus)
MERGE (nufus)-[:HAS_INFORMATION]->(cankayaNufus)
MERGE (nufus)-[:HAS_INFORMATION]->(keciorenNufus)
MERGE (nufus)-[:HAS_INFORMATION]->(mamakNufus)

// Yemekler kategorisine bilgi düğümleri ekleme
MERGE (ankaraTava:Yemek {name: "Ankara Tava"})
MERGE (bicibici:Yemek {name: "Bici Bici"})
MERGE (beypazariKurusu:Yemek {name: "Beypazarı Kurusu"})
MERGE (tirit:Yemek {name: "Tirit"})
MERGE (yemekler)-[:CONTAINS]->(ankaraTava)
MERGE (yemekler)-[:CONTAINS]->(bicibici)
MERGE (yemekler)-[:CONTAINS]->(beypazariKurusu)
MERGE (yemekler)-[:CONTAINS]->(tirit)

// Turistik yerler kategorisine bilgi düğümleri ekleme
MERGE (anitkabir:TuristikYer {name: "Anıtkabir"})
MERGE (kocatepe:TuristikYer {name: "Kocatepe Camii"})
MERGE (atakule:TuristikYer {name: "Atakule"})
MERGE (genclikParki:TuristikYer {name: "Gençlik Parkı"})
MERGE (tunalıHilmi:TuristikYer {name: "Tunalı Hilmi Caddesi"})
MERGE (turistikYerler)-[:CONTAINS]->(anitkabir)
MERGE (turistikYerler)-[:CONTAINS]->(kocatepe)
MERGE (turistikYerler)-[:CONTAINS]->(atakule)
MERGE (turistikYerler)-[:CONTAINS]->(genclikParki)
MERGE (turistikYerler)-[:CONTAINS]->(tunalıHilmi)

"""

# Sorguyu çalıştır
run_query(query)

# Bağlantıyı kapatma
driver.close()
