# Platform Setup Guide: AI/ML Remote Jobs Dataset

> **Product:** AI/ML Remote Jobs Dataset — $19
> **Data file:** `data/ai-ml-remote-jobs_latest.csv`
> **Description source:** `gumroad/product-description.md`
>
> **Credentials:**
> - Email: `ssmurfgg04@gmail.com` / Gmail app password: `jsenkqumqxqraeiw`
> - Proton email: `guyue-ai-agent@proton.me`

---

## 1. LemonSqueezy

1. Go to https://app.lemonsqueezy.com/register and sign up with your email (`ssmurfgg04@gmail.com`) and a password
2. Verify your email (check Gmail inbox)
3. Complete the onboarding — set your store name (e.g., "AI Jobs Dataset") and default currency (USD)
4. From the dashboard, click **Products** → **Create Product**
5. Set the product name to **"AI/ML Remote Jobs Dataset"**
6. Set the price to **$19 USD** (one-time purchase)
7. For description, use the HTML from `gumroad/product-description.md` — convert to rich text or paste as-is
8. Under **Variants**, ensure one variant exists (default "Default") — this is your single $19 variant
9. Upload the file **`data/ai-ml-remote-jobs_latest.csv`** as the product file/download
10. Toggle **"This is a digital product"** and set file delivery to immediate on purchase
11. Click **Save** then **Publish** (or "Make live")
12. **Product URL format:** `https://[your-store].lemonsqueezy.com/checkout/buy/[variant-id]` — you'll see the URL on the product page after publishing

### Finding your IDs after setup

- **API Key:** Settings → Developer → API Keys (copy the "API Key")
- **Store ID:** Settings → Store → store ID is in the URL or shown under General
- **Variant ID:** Products → click your product → Variants tab → variant ID shown in the URL or card

---

## 2. Ko-fi

1. Go to https://ko-fi.com and click **Sign Up**
2. Register with your Gmail (`ssmurfgg04@gmail.com`) or Proton email (`guyue-ai-agent@proton.me`)
3. Verify your email and complete the profile setup (username, display name)
4. From your dashboard, click **Shop** in the left sidebar
5. Click **Set up your shop** (if first time) — fill in shop name and description
6. Click **Add Product** → select **Digital Product**
7. Title: **"AI/ML Remote Jobs Dataset"**
8. Price: **$19.00 USD** (Ko-fi supports one-time pricing natively)
9. Upload **`data/ai-ml-remote-jobs_latest.csv`** as the downloadable file
10. Description: paste the content from `gumroad/product-description.md` (convert sections to plain text or use Ko-fi's rich editor)
11. Toggle **"This is a downloadable file"** — set delivery to automatic on purchase
12. Click **Save** then toggle the listing to **Published** (green status)
13. **Product URL format:** `https://ko-fi.com/s/[product-id]` — Ko-fi generates this after saving. You can find it under Shop → Manage Products → click the product → the URL is shown at the top

### Notes

- Ko-fi takes 0% fee (only Stripe/PayPal processing fees ~2.9% + $0.30)
- No API key needed for basic selling — everything is done through the dashboard
- You can also set up a **Commission** or **Goal** to upsell an annual subscription later ($49)

---

## 3. Payhip

1. Go to https://payhip.com and click **Get Started** (or **Sign Up**)
2. Register with your Gmail (`ssmurfgg04@gmail.com`) — free plan available
3. Verify your email and complete onboarding (store name, currency → USD)
4. From the dashboard, click **Products** → **Add Product**
5. Choose **Digital Product** as the product type
6. Product name: **"AI/ML Remote Jobs Dataset"**
7. Price: **$19.00** (one-time payment)
8. Upload **`data/ai-ml-remote-jobs_latest.csv`** under "Download File"
9. Description: paste content from `gumroad/product-description.md` — Payhip has a rich text editor that accepts HTML directly (click the `</>` icon to switch to source mode)
10. Under **Settings**, ensure:
    - "Enable Buy Button" is ON
    - "Instant download after purchase" is ON
    - Tax/VAT set to your preference (default: no tax for digital goods)
11. Click **Save** then **Publish** (toggle from Draft to Published)
12. **Product URL format:** `https://payhip.com/b/[product-code]` — e.g., `https://payhip.com/b/abc123`. You'll see it at the top of the product edit page or in Products list

### Notes

- Free plan supports unlimited products (5% + $0.50 per sale transaction fee)
- Upgrade to Plus ($29/mo) for 2% fee, affiliates, coupons, and email marketing
- **API Key:** Found in Settings → Developer → API Keys
- **Store ID:** Your Payhip store name is set during onboarding — it's the subdomain in `https://[store].payhip.com`

---

## Quick Reference

| Feature | LemonSqueezy | Ko-fi | Payhip |
|---------|-------------|-------|--------|
| Transaction fee | 5% + $0.50 | 0% (+processing) | 5% + $0.50 (free) |
| API available | Yes | Limited | Yes |
| File delivery | Auto | Auto | Auto |
| Annual upsell | Variants | Commissions | Multiple prices |
| Best for | Full control | Lowest fees | Simplicity |

**Recommended first publish:** Ko-fi (simplest, lowest fees, fastest setup).
