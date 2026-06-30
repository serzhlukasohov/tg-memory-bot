# Startup Context
_Last updated: 2024-01-15 14:30 UTC_

## What we're building
Plyn is a voice-to-text keyboard app for Polish-speaking users (including Ukrainian and Belarusian speakers in Poland). The product enables voice dictation with translation across multiple languages, powered by AI models (Gemini/Whisper). The keyboard includes text transformation modes (short, formal, warm styles) and works across any app on mobile devices. The core value proposition targets emigrants who struggle with typing in Polish or need quick voice-based text input.

## Current Status
**Pre-launch phase** - Website deployed at plyn.click, app development ~95% complete. Team is in aggressive shipping mode, focusing on core functionality over nice-to-haves. Currently building financial model and unit economics while preparing for marketing validation. Critical bugs (text insertion failures, connection drops) have been identified and need resolution before user acquisition begins. Marketing strategy decision pending expert consultation on email capture vs. paid pre-orders. ASO/ASA identified as promising growth channel (~$200/geo).

**Active priorities:**
- Complete response styles feature implementation
- Create product demo video
- Build financial model structure (MD/CSV format, then migrate to Google Sheets)
- Schedule ASO/ASA expert consultation
- Resolve infrastructure issues (git authentication, gog tool installation)

## Key Decisions Made
1. **Domain & Deployment**: Deployed public website to plyn.click (corrected from initial plin.click typo)
2. **Scope Management**: Deprioritized dashboard, full keyboard, advanced activation features to focus on core voice input
3. **Marketing Strategy**: Paused email capture development pending expert consultation on validation approach (simple email list vs. paid pre-orders)
4. **Financial Planning**: Use Google Sheets as source of truth for financial models with MD summary in wiki
5. **Interim Process**: Build financial model in MD/CSV first due to gog tool unavailability, migrate to Sheets later
6. **Bug Classification**: Text mode locale issue classified as UX bug requiring fix, not feature enhancement
7. **Launch Blocker**: Identified two critical bugs (text insertion, connection drops) that must be fixed before user acquisition
8. **Task Management**: Moving toward structured task tracking via wiki-based board system
9. **Documentation Strategy**: Separating interactive financial models (Sheets) from explanatory summaries (wiki)
10. **Pre-launch Domain**: Acquired plinklink.com via Cloudflare (€9.05) as placeholder during setup

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in Polish market and advertising activity?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?

**Pricing & Business Model:**
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for similar subscriptions?
- Should pricing be displayed on waitlist landing page?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - per country or more granular?
- Should we do simple email list or paid pre-orders for validation?

**Unit Economics & Usage:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens/minute or 30 tokens/minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on subscription plans?
- Is there open analytics data on user monthly minute requirements?

**Technical & Product:**
- Which AI model performs best for Polish - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and target languages?
- Is it technically possible to access conversation context from custom keyboard on mobile?
- Can on-device models like Gemini's local version work for non-English languages?
- Why does language detection/switching work inconsistently?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Market Research:**
- Can we find underserved niche (e.g., emigrants who don't know local language)?
- How popular are voice messages in messengers and what's demand for voice-to-text conversion?
- How to record demo video - with hands or just screencast?

**Infrastructure & Process:**
- How to configure GitHub authentication for Plyn Bot to enable push operations?
- When will gog be installed and authorized in workspace?
- Should Google Sheet be created manually or wait for gog installation?
- How should wiki documentation be kept in sync with new features?

## Next Actions

**Product Development:**
- Fix critical bug: dictated text doesn't insert
- Fix critical bug: companion app connection requires restart (red light indicator)
- Implement response styles (warm, friendly, etc.) in the app
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Merge pending pull requests
- Debug system prompt for inconsistent language detection behavior
- Update system prompt in Firebase
- Implement authentication system
- Investigate direct keyboard voice activation feasibility

**Marketing & Launch:**
- Create product demo video
- Schedule ASO/ASA mentor call with Yan
- Schedule call with marketing contact on ASO/ASA model and pre-order strategy
- Complete landing page design/development on plyn-site.vercel.app
- Set up email collection worker for landing page waitlist (paused pending strategy decision)
- Set up Cloudflare Pages CI for website deployment

**Market Research:**
- Research Grammarly's penetration and advertising in Polish market
- Manually verify Google search results for Polish keyboard queries
- Generate 3-5 killer features for emigrants who don't speak Polish well
- Research pricing Polish/Ukrainian/Belarusian users pay for subscriptions
- Perform competitor analysis (Wispr Flow, VoiceInk): value props, features, marketing, pricing
- Calculate cost per hour based on token usage, verify counting methodology
- Find analytics on typical user monthly usage patterns
- Test which AI model performs best for Polish
- Test Whisper v3 and Gemini with Polish and other target languages
- Research where to find target audience (Telegram expat groups, Facebook groups)
- Analyze voice message usage and transcription demand in WhatsApp/Telegram
- Watch JTBD video tutorial
- Ask friend launching text-to-speech startup about market insights

**Financial Planning:**
- Build financial model structure in MD/CSV format (assumptions, pricing, usage, costs, scenarios, formulas)
- Create financial model and unit economics calculations in Google Sheets with wiki summary (after gog available)

**Infrastructure & Operations:**
- Configure GitHub authentication (SSH keys/PAT) for Plyn Bot's workspace
- Push local commit d45d1bb from environment with GitHub access
- Install and authorize gog tool in workspace environment
- Fix authentication and user mapping in sandbox for git access
- Grant admin access to Yanka for the group

**Localization & Testing:**
- Find Polish native speaker to verify localization
- Rebuild/redraw APK after adding Polish language
- Add serzh to TestFlight

**Planning & Coordination:**
- Schedule sync call to create timeline and roadmap (2-3 week sprint to landing page launch)
- Create schematic launch plan for team review
- Finalize mountain route; share elevation profile with Yan