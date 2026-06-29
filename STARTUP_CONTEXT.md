# Startup Context
_Last updated: 2024-12-20 10:30 UTC_

## What we're building
Plyn is a mobile-first AI voice keyboard targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines real-time voice dictation with AI beautification and translation capabilities across multiple languages. Unlike competitors focusing on English desktop markets, Plyn addresses an underserved emigrant community niche where existing solutions (including Grammarly, which only added Polish in March 2026) aren't actively marketing. The product works as a system-wide keyboard replacement with voice-to-text that not only transcribes but enhances spoken input with superior translation quality compared to Google Translate. Current implementation uses Gemini API (gemini-2.5-flash model) with unit economics showing €5/month can support ~4 hours of usage.

## Current Status
**Phase:** Critical bug fixing before market launch
**Distribution:** Closed TestFlight with invitation codes
**Supported Languages:** Polish, Russian (Belarusian and Ukrainian in testing)
**Immediate Priority:** Fix show-stopping bugs (text insertion failures, companion app connection drops) that will prevent user retention. Team is dogfooding the product and implementing structured task tracking to prevent work from getting lost in conversations.

**Shipping Philosophy:** Aggressive speed-to-market approach, consciously deprioritizing dashboard, full keyboard features, and advanced activation to focus on core voice input functionality. Moving from fake door landing page validation to functional MVP before competitors enter the Polish market window.

## Key Decisions Made
1. **Market Pivot** - Abandoned saturated English desktop market for blue ocean Polish/Ukrainian/Belarusian mobile niche
2. **Belarusian Language Hook** - Identified as viral GTM opportunity (no mobile keyboards currently support it)
3. **Cloud-First Architecture** - Prioritized speed over privacy with cloud-based MVP vs on-device processing
4. **Lean Validation** - Committed to fake door landing page before full product build (2-3 week timeline)
5. **Feature Deprioritization** - Dashboard, style selection post-transcription, and direct voice activation deferred
6. **Quality Gate** - Will not launch marketing until critical bugs fixed to avoid permanent user loss
7. **Multi-Language Support** - Added Polish alongside Russian with translation capabilities
8. **UX Polish** - Implemented haptic and audio feedback for paste/insert actions
9. **System Prompt Fix** - Stabilized multilingual behavior across all supported languages
10. **Process Structure** - Moving to board-based task tracking (potentially wiki) to prevent lost work

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?

**Pricing & Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Should pricing be displayed on the waitlist landing page?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Can GitBook's free tier support the team's requirements?
- Can I update the system prompt in Firebase, and is there versioning/rollback support if the previous version needs to be restored?
- How should authentication be implemented?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?

**Product & UX:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- How to properly record demo video - with hands or just screencast?
- When should proper user research be conducted for the feature?

## Next Actions

**Critical Path (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets

**Product Development:**
- Merge the pending pull requests
- Test the updated system prompt across all languages
- Test translation feature with Belarusian and Russian languages
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Update system prompt in Firebase
- Add serzh to TestFlight

**Business & Planning:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together in next call

**Landing Page & Marketing:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw

**Technical Investigation:**
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Evaluate GitBook and its free tier capabilities
- Investigate if direct keyboard voice activation is possible

**Process & Knowledge:**
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights