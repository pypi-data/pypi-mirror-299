from server import HybridComputeSDK

async def get_price(params):
    # This is a mock implementation. Replace with actual logic.
    return f"The price for {params['string']} is $10.00"

if __name__ == "__main__":
    hybrid_compute = (
        HybridComputeSDK()
        .create_json_rpc_server_instance()
        .add_server_action('getprice(string)', get_price)
        .listen_at(1234)
    )

    print(f"Started successfully: {hybrid_compute.is_server_healthy()}")