
from pymilvus import MilvusClient, DataType
import random

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)


def create_collection():
    client.drop_collection("filtered_search_collection")

    schema = client.create_schema(enable_dynamic_field=True)
    schema.add_field("id", DataType.INT64, is_primary=True, auto_id=False)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=5)

    index_params = client.prepare_index_params()
    index_params.add_index(field_name="vector",
                           index_type="FLAT",
                           metric_type="IP")

    client.create_collection(collection_name="filtered_search_collection",
                             schema=schema,
                             index_params=index_params,
                             consistency_level="Bounded")

    rows = [
        {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "color": "pink_8682", "likes": 165},
        {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "color": "red_7025", "likes": 25},
        {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "color": "orange_6781", "likes": 764},
        {"id": 3, "vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345], "color": "pink_9298", "likes": 234},
        {"id": 4, "vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184, 0.30337481143159106], "color": "red_4794", "likes": 122},
        {"id": 5, "vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383, -0.1446277761879955], "color": "yellow_4222", "likes": 12},
        {"id": 6, "vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192, -0.8984947637863987], "color": "red_9392", "likes": 58},
        {"id": 7, "vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709, 0.5378064918413052], "color": "grey_8510", "likes": 775},
        {"id": 8, "vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872, -0.6140360785406336], "color": "white_9381", "likes": 876},
        {"id": 9, "vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717, -0.6980531615588608], "color": "purple_4976", "likes": 765}
    ]
    client.insert(collection_name="filtered_search_collection", data=rows)

    res = client.query(collection_name="filtered_search_collection",
                       filter="",
                       output_fields=["count(*)"],
                       consistency_level="Strong")
    print(res)


def filtered_search():
    query_vector = [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]

    res = client.search(
        collection_name="filtered_search_collection",
        data=[query_vector],
        limit=5,
        # highlight-start
        filter='color like "red%" and likes > 50',
        output_fields=["color", "likes"]
        # highlight-end
    )

    for hits in res:
        print("TopK results:")
        for hit in hits:
            print(hit)


if __name__ == "__main__":
    create_collection()
    print("================ filtered_search ================")
    filtered_search()
