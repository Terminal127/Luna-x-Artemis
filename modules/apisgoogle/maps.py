import os

subscription_key = ""

def search_point_of_interest_category():
    from azure.core.credentials import AzureKeyCredential
    from azure.maps.search import MapsSearchClient
    from azure.maps.render import MapsRenderClient
    from azure.maps.render.models import TilesetID, BoundingBox
    import boundingbox as bb

    # Initialize clients
    credential = AzureKeyCredential(subscription_key)
    maps_render_client = MapsRenderClient(credential=credential)
    maps_search_client = MapsSearchClient(credential=credential)

    # Search for a point of interest
    result = maps_search_client.search_point_of_interest("barbeque nation, bhubaneswar")
    # print(dir(result.results[0]))
    # for res in dir(result.results[0]):
    #     print (res)
    print(result.results[0].address)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].id)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].detour_time)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].data_sources)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].distance_in_meters)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].info)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].viewport)
    print("------------------------------------------------------------------------------------------------")
    print(result.results[0].point_of_interest)
    print("------------------------------------------------------------------------------------------------")
    
    # print(result.results[0].id)
    # Obtain bounding box values
#     latMin, lonMin, latMax, lonMax = bb.boundingBox(result.results[0].position.lat, result.results[0].position.lon, 1)

# # Create a BoundingBox instance manually
#     bounding_box_instance = BoundingBox(south=latMin, west=lonMin, north=latMax, east=lonMax)
#     print(result.results[0].position)

#     try:
#         # Get map static image
#         render_result = maps_render_client.get_map_attribution(
#         tileset_id=TilesetID.MICROSOFT_BASE,
#         zoom=6,
#         bounds=BoundingBox(
#             south=42.982261,
#             west=24.980233,
#             north=56.526017,
#             east=1.355233
#         )
#     )

#         print("Get map tile result to png file as 'map_static_image.png'")
#         # Save result to file as png
#         with open('map_static_image.png', 'wb') as file:
#             file.write(next(render_result))

#     except Exception as e:
#         print(f"Error: {e}")

if __name__ == '__main__':
    search_point_of_interest_category()
