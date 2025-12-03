import re

class Chatbot:
    def __init__(self, services):
        self.services = services
        self.context = {}

    def update_context(self, user_role, current_page):
        self.context['role'] = user_role
        self.context['page'] = current_page

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # --- 1. Greetings ---
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'start', 'hola', 'مرحبا', 'اهلين', 'سلام']):
            return "Hello! 👋 I'm the Service Connect Assistant. I can help you with:\n- Browse services & prices\n- Book a service\n- Check order status\n- Account help"

        # --- 2. Services & Pricing ---
        if any(word in user_input for word in ['service', 'price', 'cost', 'how much', 'list', 'offer', 'cleaning', 'plumbing', 'tech']):
            response = "📋 **Available Services:**\n\n"
            for s in self.services:
                response += f"🔹 **{s['name']}** - ${s['price']} ({s['category']})\n"
            response += "\n💡 Login as a User to book any service!"
            return response

        # --- 3. Booking / How to Order ---
        if any(word in user_input for word in ['book', 'order', 'reserve', 'buy', 'schedule', 'how']):
            if self.context.get('role') == 'user':
                return "📝 **To book a service:**\n1. Go to Services page\n2. Click 'Select' on a service\n3. Fill the booking form\n4. Confirm!"
            elif self.context.get('role') == 'technical':
                return "⚠️ As a Technical expert, you provide services, not book them. Check the Pending Orders page."
            else:
                return "🔑 Please **Login** or **Register** as a User to book services."

        # --- 4. Technical / Orders ---
        if any(word in user_input for word in ['pending', 'job', 'work', 'task', 'order']):
            if self.context.get('role') == 'technical':
                return "🛠️ View all jobs in **Pending Orders**. Click 'Mark as Done' when you finish."
            elif self.context.get('role') == 'user':
                return "📦 Check your bookings in **My Orders** page."
            else:
                return "🔑 Please login to view orders."

        # --- 5. Account ---
        if any(word in user_input for word in ['login', 'sign in', 'register', 'sign up', 'account']):
            return "👤 **Account Options:**\n- **User**: Book services\n- **Technical**: Provide services\n\nGo to Home page to Login or Register."

        # --- 6. About ---
        if any(word in user_input for word in ['about', 'who', 'company', 'mission']):
            return "🏢 **Service Connect** - Connecting local professionals with clients. Home, Tech, Auto & Maintenance services."

        # --- Default Fallback ---
        return "❓ I can help with:\n- Services & Prices\n- How to Book\n- Account Help\n- Order Status\n\nJust ask me anything!"
