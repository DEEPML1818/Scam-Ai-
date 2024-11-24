import json
import random

# Scam categories, evidence, and languages
scam_types = [
    "fake investments and Ponzi schemes",
    "phishing attacks via emails",
    "fraudulent e-commerce websites",
    "crypto pump-and-dump schemes",
    "lottery scams and fake winnings",
    "identity theft and impersonation",
    "job offer scams requiring payments",
    "charity scams exploiting disasters"
]

evidence_types = [
    "Reported by financial authorities.",
    "Multiple complaints from victims.",
    "Tracked by cybersecurity experts.",
    "Evidence gathered by consumer protection agencies.",
    "Investigated by fraud detection teams."
]

translations = {
    "fake investments and Ponzi schemes": {
        "Malay": "Pelaburan palsu dan skim Ponzi",
        "Chinese": "虚假投资和庞氏骗局",
        "Tamil": "போன்ஸி திட்டங்கள் மற்றும் பாசாங்கு முதலீடுகள்"
    },
    "phishing attacks via emails": {
        "Malay": "Serangan pancingan data melalui e-mel",
        "Chinese": "通过电子邮件的网络钓鱼攻击",
        "Tamil": "மின்னஞ்சல் மூலம் புரோவோஷிங் தாக்குதல்"
    },
    "fraudulent e-commerce websites": {
        "Malay": "Laman web e-dagang palsu",
        "Chinese": "欺诈性的电子商务网站",
        "Tamil": "மோசடி ஆன்லைன் வணிக தளங்கள்"
    },
    "crypto pump-and-dump schemes": {
        "Malay": "Skim pump-and-dump kripto",
        "Chinese": "加密货币的拉高出货骗局",
        "Tamil": "கிரிப்டோ பம்ப் மற்றும் டம்ப் திட்டங்கள்"
    },
    "lottery scams and fake winnings": {
        "Malay": "Penipuan loteri dan kemenangan palsu",
        "Chinese": "彩票诈骗和虚假中奖",
        "Tamil": "லாட்டரி மோசடி மற்றும் பாசாங்கு வெற்றி"
    },
    "identity theft and impersonation": {
        "Malay": "Kecurian identiti dan penyamaran",
        "Chinese": "身份盗用和冒充",
        "Tamil": "அடையாள திருட்டு மற்றும் பாசாங்கு"
    },
    "job offer scams requiring payments": {
        "Malay": "Penipuan tawaran kerja memerlukan pembayaran",
        "Chinese": "要求付款的工作机会诈骗",
        "Tamil": "செலுத்தல் தேவைப்படும் வேலை வாய்ப்பு மோசடிகள்"
    },
    "charity scams exploiting disasters": {
        "Malay": "Penipuan amal yang mengeksploitasi bencana",
        "Chinese": "利用灾难的慈善骗局",
        "Tamil": "ஆபத்துக்களை ஆளாக்கும் தொண்டு மோசடிகள்"
    }
}

# Generate random scam data
def generate_scam_data(num_entries=50):
    scam_data = []
    for _ in range(num_entries):
        scam_type = random.choice(scam_types)
        evidence = random.choice(evidence_types)
        company_name = f"{random.choice(['ABC', 'XYZ', 'Global', 'Trusted', 'FastTrack', 'Premium'])} {random.choice(['Ventures', 'Holdings', 'Group', 'Solutions', 'Partners', 'Corporation'])}"
        scam_entry = {
            "company_name": company_name,
            "description": {
                "English": scam_type,
                "Malay": translations[scam_type]["Malay"],
                "Chinese": translations[scam_type]["Chinese"],
                "Tamil": translations[scam_type]["Tamil"]
            },
            "scam_status": "Scam",
            "evidence": evidence
        }
        scam_data.append(scam_entry)
    return scam_data

# Save data to JSON file
def save_to_json(data, filename="scams.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Generate and save
scam_data = generate_scam_data(50)
save_to_json(scam_data)
print("Scam data has been generated and saved to scams.json!")
