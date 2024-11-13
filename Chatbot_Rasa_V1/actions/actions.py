from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import random  # For simulating order status


class ActionCheckOrderStatus(Action):
    def name(self):
        return "action_check_order_status"

    def run(self, dispatcher, tracker, domain):
        # Retrieve the order number from the slot
        order_number = tracker.get_slot('order_number')

        # Check if the order number exists
        if order_number:
            # Simulate an order status (replace this with real API logic if available)
            status_options = ["Shipped", "In Transit", "Out for Delivery", "Delivered"]
            order_status = random.choice(status_options)

            # Send the response back to the user
            dispatcher.utter_message(text=f"Order {order_number} is currently: {order_status}.")
        else:
            # If no order number is provided
            dispatcher.utter_message(text="I couldn't find your order number. Please try providing it again.")

        # Return an empty list of events
        return []

class ActionVerifyAndCheckOrderStatus(Action):
    def name(self):
        return "action_verify_and_check_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Retrieve the slots for order number and email
        order_number = tracker.get_slot("order_number")
        email = tracker.get_slot("email")

        # Simulated order database
        order_data = {
            "12345": {"email": "user@example.com", "status": "Shipped"},
            "67890": {"email": "anotheruser@example.com", "status": "In Transit"},
            "54321": {"email": "user@example.com", "status": "Delivered"},
        }

        # Check if the order number exists in the database
        if order_number in order_data:
            # Verify that the provided email matches the one on file for this order
            if order_data[order_number]["email"] == email:
                # Retrieve the order status
                order_status = order_data[order_number]["status"]
                dispatcher.utter_message(
                    text=f"Order {order_number} is currently: {order_status}."
                )
            else:
                dispatcher.utter_message(
                    text="The email you provided does not match our records for this order. Please check and try again."
                )
        else:
            dispatcher.utter_message(
                text="The order number you provided does not exist in our records. Please check the order number and try again."
            )

        # Clear the slots after checking
        return [SlotSet("order_number", None), SlotSet("email", None)]


class ActionRecommendProduct(Action):
    def name(self):
        return "action_recommend_product"

    def run(self, dispatcher, tracker, domain):
        product_type = tracker.get_slot("product_type")
        budget = tracker.get_slot("budget")

        if product_type and budget:
            dispatcher.utter_message(text=f"Here are some {product_type}s under ${budget}.")
        elif product_type:
            dispatcher.utter_message(text=f"Here are some popular {product_type}s.")
        else:
            dispatcher.utter_message(text="Tell me what type of product you’re looking for.")
        return []

class ActionCancelOrder(Action):
    def name(self):
        return "action_cancel_order"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot("confirm_cancellation"):
            dispatcher.utter_message(text="Your order has been canceled.")
        else:
            dispatcher.utter_message(text="Order cancellation has been aborted.")
        return [SlotSet("confirm_cancellation", None)]

