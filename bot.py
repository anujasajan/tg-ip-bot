from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import socket

BOT_TOKEN = "8461335437:AAGctKHd928dGTLfWWrYJSzTkD1PsxpdPhw"  # <-- ඔයාගේ token එක මෙතන දාන්න

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm your IP & Domain lookup bot.\n\n"
        "Commands:\n"
        "🔹 /myip → Show your public IP 🌍\n"
        "🔹 /ip <address> → Lookup any IP address 🔍\n"
        "🔹 /domain <domain> → Get IP of a domain 🖥️"
    )

# /ip command
async def ip_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: /ip <IP address>")
        return

    ip = context.args[0]
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=query,country,regionName,city,isp,status,message").json()

        if res.get("status") == "fail":
            await update.message.reply_text(f"⚠️ Error: {res.get('message')}")
            return

        msg = f"""
🌍 **IP Lookup Result**
🆔 IP: `{res.get('query')}`
🏳️ Country: {res.get('country')}
🏙️ Region: {res.get('regionName')}
🏡 City: {res.get('city')}
🏢 ISP: {res.get('isp')}
"""
        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error checking IP: {e}")

# /domain command
async def domain_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: /domain <example.com>")
        return

    domain = context.args[0]
    try:
        ip_addr = socket.gethostbyname(domain)
        msg = f"🌐 Domain: `{domain}`\n🆔 IP Address: `{ip_addr}`"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error resolving domain: {e}")

# /myip command
async def myip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://ipinfo.io/json").json()
        msg = f"""
🌐 **Your IP Info**
🆔 IP: `{res.get('ip','N/A')}`
🏙 City: {res.get('city','N/A')}
🌍 Region: {res.get('region','N/A')}
🏳️ Country: {res.get('country','N/A')}
🏢 ISP: {res.get('org','N/A')}
"""
        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error checking your IP: {e}")

# Build bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ip", ip_lookup))
app.add_handler(CommandHandler("domain", domain_lookup))
app.add_handler(CommandHandler("myip", myip))

print("🤖 Bot is running...")
app.run_polling()
