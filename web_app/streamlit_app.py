import requests
import streamlit as st


def app():
    st.title("Hello it is Demand Forecast servis!")

    # Make variables for user input
    sku_id = st.number_input("Enter SKU ID:", value=1)
    stock = st.number_input("Enter Stock:", value=10)
    horizon_days = st.slider(
        "Enter Horizon Days:", min_value=7, max_value=21, value=7, step=7
    )
    confidence_level = st.slider(
        "Select Confidence Level:", min_value=0.1, max_value=0.9, value=0.1, step=0.4
    )
    payload = {
        "sku": {"sku_id": int(sku_id), "stock": stock},
        "horizon_days": horizon_days,
        "confidence_level": confidence_level,
    }
    payload_list = {
        "confidence_level": confidence_level,
        "horizon_days": horizon_days,
        "sku_stock": [{"sku_id": int(sku_id), "stock": stock}],
    }

    # Make buttons for user input
    if st.button("Get how much to order"):
        # Make request
        send_request("http://app:8000/api/how_much_to_order", payload)

    if st.button("Get stock level forecast"):
        # Make request
        send_request("http://app:8000/api/stock_level_forecast", payload)

    if st.button("Get low stock sku list"):
        # Make request
        send_request("http://app:8000/api/low_stock_sku_list", payload_list)


def send_request(url, payload):
    """Send request to FastAPI server"""
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.write(f"{response.json()}")
        else:
            st.write(
                f"Failed to get response from FastAPI server ({url}). Status code: {response.status_code}"
            )
    except Exception as e:
        st.write(f"An error occurred: {e}")


if __name__ == "__main__":
    app()
