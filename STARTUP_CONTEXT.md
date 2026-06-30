# Startup Context
_Last updated: 2025-01-24_

## What we're building

Plyn is a voice-first Polish keyboard app with AI-powered text beautification and multi-language support. The product targets Polish, Ukrainian, and Belarusian language speakers in Poland, positioning against Grammarly with differentiation through voice input and real-time translation capabilities. 

The app features real-time voice dictation, translation between multiple languages (Polish, Russian, Ukrainian, Belarusian), and AI text enhancement superior to Google Translate. Belarusian language support serves as a potential viral growth hook since no mobile keyboards currently support it.

Currently in closed TestFlight testing phase. Public website deployed at plyn.click. The product is nearly launch-ready with only response styles feature remaining before market entry.

## Current Status

**Product Development:** App functionally complete with working voice dictation, translation, and text beautification. Authentication implemented. Critical bugs fixed (text insertion, companion app connection). UI polished with haptic and audio feedback. Only response styles feature remains before launch readiness.

**Go-to-Market:** Website deployed at plyn.click with domain secured. Team pausing at strategic inflection point to consult marketing experts before choosing validation approach (simple email collection vs. paid pre-orders). ASO/ASA identified as promising growth channel pending cost structure clarity.

**Infrastructure:** Plyn Bot operational for project management but blocked by SSH authentication issues preventing automated git operations.

**Strategy:** Aggressive shipping mode - deprioritizing dashboard, full keyboard, advanced activation to focus on core voice input. Strong emphasis on speed to market due to competitive pressure (Grammarly added Polish support March 2026, market window closing).

## Key Decisions Made

1. **Market pivot to Polish/Ukrainian/Belarusian speakers in Poland** - Identified clear market opportunity with Grammarly only adding Polish support in March 2026 and no active Polish marketing from competitors
2. **Voice-first positioning** - Differentiate from Grammarly through voice input rather than typing
3. **Belarusian as viral hook** - No mobile keyboards support Belarusian, potential unique selling point
4. **Lean validation approach** - Fake door landing page before building full product (compressed to 2-3 week timeline)
5. **Critical bugs before users** - Must fix stability issues before acquisition as they cause permanent churn
6. **Aggressive feature deprioritization** - Ship core voice input first, defer dashboard/full keyboard/advanced activation
7. **Domain acquisition** - Secured plyn.click as public domain (corrected from initial plin.click typo)
8. **Pause email capture** - Wait for marketing strategy decision before implementing waitlist functionality
9. **Expert consultation before launch** - Consulting ASO/ASA experts and marketing contacts before choosing between simple email list vs. paid pre-orders
10. **Dogfooding own product** - Team actively using voice keyboard internally for validation

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Which AI model performs best for Polish language - likely Google/Gemini?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

**Pricing & Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many users need per month?

**Marketing & Distribution:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?
- How to properly record demo video - with hands or just screencast?

**Product & Technical:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?

**Infrastructure & Tools:**
- Can GitBook's free tier support the team's requirements?
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?
- How to resolve the user mapping issue (uid 501) in sandbox environment to enable git push operations?

## Next Actions

**Critical Path (Launch Blockers):**
- Implement response styles (warm, friendly, etc.) in the app
- Create product demo video
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Marketing strategy decision needed before unpausing email capture

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers

**Financial Modeling:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Product Validation:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Test which AI model performs best for Polish language generation
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Distribution Research:**
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Schedule ASO/ASA mentor call with Yan

**Localization:**
- Find Polish native speaker to verify localization

**Infrastructure:**
- Configure GitHub authentication (SSH keys or personal access token) for Plyn Bot's workspace environment
- Fix authentication and user mapping in sandbox environment to enable remote git access
- Push local commit d45d1bb from environment with GitHub access
- Evaluate GitBook and its free tier capabilities

**Planning:**
- Schedule sync call to create timeline and roadmap
- Create schematic launch plan to review together in next call

**Deferred/Lower Priority:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Investigate if direct keyboard voice activation is possible
- Set up Cloudflare Pages CI for website