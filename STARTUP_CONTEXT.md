# Startup Context
_Last updated: 2025-01-24 14:30 UTC_

## What we're building
Plyn is a mobile-first voice-to-text keyboard with AI beautification for Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product differentiates from Grammarly (which only added Polish in March 2026) through voice-first input and multi-language support for emigrant communities. The app uses Gemini API for audio and text processing, offering real-time dictation with translation capabilities and AI-enhanced formatting. Target pricing is €5/month supporting ~4 hours of usage. Public website deployed at plyn.click.

## Current Status
**Phase:** Pre-launch validation and final product polish

**Immediate priorities:**
- Response styles feature (last major feature before launch readiness)
- ASO/ASA marketing strategy consultation scheduled
- Product demo video creation
- Marketing validation approach decision (email list vs. paid pre-orders)

**Technical state:**
- App in closed TestFlight testing
- Core dictation and translation working across Polish, Ukrainian, Russian, Belarusian
- Critical bugs fixed; authentication implemented
- Website deployed to plyn.click domain
- Plyn Bot operational but blocked on git authentication for automated push operations

**Blockers:**
- Marketing strategy decision needed before enabling email capture
- Git authentication preventing Plyn Bot from pushing documentation updates

## Key Decisions Made
1. **Market pivot** - Target Polish/Ukrainian/Belarusian speakers in Poland instead of English desktop market (blue ocean strategy)
2. **Voice-first positioning** - Compete against Grammarly with voice input as differentiator
3. **Cloud-first MVP** - Prioritize speed to market over on-device privacy
4. **Belarusian support** - Include as viral GTM hook (no mobile keyboards currently support it)
5. **Lean validation** - Use fake door landing page before building full product
6. **Feature discipline** - Deprioritize dashboard, full keyboard, advanced activation for speed
7. **Domain strategy** - Deployed to plyn.click (corrected from initial plin.click typo)
8. **Critical bugs first** - Must fix blocking issues before user acquisition to prevent churn
9. **Pause email capture** - Hold until marketing strategy consultation complete
10. **Unit economics baseline** - €5/month targets ~4 hours usage with viable margins

## Open Questions
**Market & Competition:**
- What is Grammarly's penetration in Polish market and are they actively advertising?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- What average price point do Polish/Ukrainian/Belarusian users in Poland pay for subscription products?

**Marketing & Distribution:**
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - per country or more granular?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation)?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- How to record demo video - with hands or just screencast?

**Technical & Product:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Is it technically possible to access conversation context from custom keyboard on mobile?
- Can on-device models like Gemini's local version work for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?

**Unit Economics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**User Research:**
- How popular are voice messages in different messengers and what's demand for transcription?
- Can we find underserved niche/use case (e.g., emigrants who don't know local language)?
- When should proper user research be conducted?

## Next Actions
**Critical Path (Launch Blockers):**
- Implement response styles (warm, friendly, etc.) in the app
- Create product demo video
- Schedule/complete ASO/ASA mentor call with Yan
- Finalize marketing strategy decision (email list vs. pre-orders)

**Marketing & Validation:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research pricing - what target users typically pay for subscription products
- Research where to find and engage target audience (Telegram expat groups, Facebook groups in Warsaw/Wroclaw)
- Set up email collection worker for landing page waitlist (after strategy decision)

**Product & Technical:**
- Fix git authentication for Plyn Bot push operations
- Push local commit d45d1bb with domain corrections from environment with GitHub access
- Test which AI model performs best for Polish language generation
- Find Polish native speaker to verify localization
- Watch JTBD (Jobs-to-be-Done) video tutorial
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Investigate if direct keyboard voice activation is possible
- Test Whisper v3 and Gemini model performance with Polish and other target languages

**Business Planning:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)

**Competitor Research:**
- Perform competitor analysis of Wispr Flow, VoiceInk, and others (value propositions, features, marketing, pricing)
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support Polish, Ukrainian, Russian markets
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, other messengers

**Infrastructure & Operations:**
- Set up Cloudflare Pages CI for website
- Schedule sync call to create timeline and roadmap
- Finalize mountain route; share elevation profile with Yan
- Ask friend launching text-to-speech startup about market insights