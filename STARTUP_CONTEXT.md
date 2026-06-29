# Startup Context
_Last updated: 2024-12-20 10:30 UTC_

## What we're building
Plyn is a mobile-first voice-to-text keyboard for Polish, Ukrainian, Russian, and Belarusian speakers in Poland. The product goes beyond basic transcription by adding an AI beautification layer that enhances spoken input - similar to Grammarly but differentiated by voice-first input and multi-language support for emigrant communities. The app uses Gemini API for real-time voice dictation with translation capabilities and works as a custom keyboard across messaging apps.

The positioning targets a blue ocean opportunity: Grammarly only added Polish support in March 2026, and no competitors are actively marketing Polish-language voice keyboards. Belarusian language support (currently unsupported by any mobile keyboard) serves as a potential viral go-to-market hook.

## Current Status
**Strategic inflection point on go-to-market validation.** The team is pausing before website launch to consult marketing experts on the optimal validation approach - simple email collection versus paid pre-orders at discounted rates (5 PLN for first 3 months). Domain secured (plinklink.com), website ready, app development nearly complete (only response styles remaining).

**ASO/ASA identified as promising growth channel** pending cost structure analysis. Unit economics established at €5/month supporting ~4 hours usage. Current monthly costs minimal (€0.53 in April 2026).

**Taking measured, expert-guided approach** to de-risk launch rather than rushing to market. Team in aggressive shipping mode, consciously deprioritizing non-core features (dashboard, full keyboard features, advanced activation) to focus on core voice input functionality.

**Active dogfooding phase** - team using their own product with recent fixes to multilingual support and UI polish (haptic/audio feedback). Critical bugs previously blocking user research have been addressed.

## Key Decisions Made
1. **Market pivot to underserved non-English languages** - Abandoned saturated English desktop voice-to-text market for Polish/Ukrainian/Russian/Belarusian mobile-first opportunity (blue ocean strategy)
2. **Focused positioning against Grammarly** - Voice-first AI beautification for emigrant communities rather than developer tools or general transcription
3. **Lean validation with fake door landing page** - Testing demand before building full product (2-3 week sprint timeline)
4. **Cloud-based MVP over on-device privacy** - Prioritizing speed to market, targeting non-technical users who pay for convenience
5. **Belarusian language as viral hook** - Only mobile keyboard supporting Belarusian, potential viral growth in underserved community
6. **Critical bugs must be fixed before user acquisition** - Recognition that launching with bugs causes permanent user loss
7. **Aggressive feature deprioritization** - Dashboard, style selection after transcription, direct voice activation from keyboard all deprioritized
8. **Domain acquisition** - Secured plinklink.com via Cloudflare for €9.05 as placeholder
9. **Pause on email capture implementation** - Deliberately waiting for expert marketing consultation before choosing validation approach
10. **Structured task tracking** - Moving from conversational task management to board system (wiki-based) to prevent items getting lost

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Pricing & Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Should pricing be displayed on the waitlist landing page?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Product & Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Go-to-Market:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- Where to find and engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw?
- How to properly record demo video - with hands or just screencast?

**Tooling:**
- Can GitBook's free tier support the team's requirements?
- Should we set up a task board through wiki or another tool?
- What name, vibe, and emoji should be assigned to Plyn Bot?

## Next Actions

**Critical Path - Marketing Strategy:**
- Consult marketing experts on email collection vs. paid pre-orders approach
- Research ASO/ASA cost structure and viability as growth channel
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw

**Product Development:**
- Complete response styles implementation (final feature before launch readiness)
- Set up email collection worker for landing page waitlist (pending strategy decision)
- Record real demo video on actual device showing the keyboard in action
- Replace the video on the website
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation

**Market Research & Analysis:**
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Find open analytics on typical user monthly usage patterns
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well

**Financial Modeling:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology

**Localization & Quality:**
- Find Polish native speaker to verify localization

**Domain & Infrastructure:**
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)

**Project Management:**
- Set up a task board system (possibly through wiki)
- Schedule sync call to create timeline and roadmap
- Create schematic launch plan to review together in next call
- Provide bot configuration (name/vibe/emoji) or review suggested options

**Research & Learning:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights
- Evaluate GitBook and its free tier capabilities

**Technical Investigation:**
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets