# Startup Context
_Last updated: 2024-12-19 14:30 UTC_

## What we're building
A mobile-first voice dictation keyboard with AI beautification and translation capabilities, targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product differentiates from competitors like Grammarly (which only added Polish in March 2026) through voice-first input, multi-language support for emigrant communities, and superior translation quality. Core functionality includes real-time voice transcription, AI-enhanced text formatting, and cross-language translation. Currently deployed via TestFlight in closed testing phase using Gemini API (gemini-2.5-flash model) with €5/month economics supporting ~4 hours of usage.

## Current Status
**Phase:** Pre-launch validation and stabilization

**Critical blockers identified:**
- Dictated text sometimes fails to insert into target applications
- Companion app frequently loses connection, requiring manual restarts
- Authentication system not yet implemented

**Recent progress:**
- Polish language support added and working
- Translation functionality fixed and tested (quality superior to Google)
- UI polished with haptic and audio feedback
- Multilingual system prompt fixed
- Team actively dogfooding the product

**Strategic focus:** Shipping speed prioritized over feature completeness. Deprioritizing dashboard, full keyboard features, and advanced activation to focus on core voice input. Landing page validation planned for 2-3 week timeline to capture market before competitors enter Polish space.

## Key Decisions Made
1. **Market pivot** - Targeting Polish/Ukrainian/Belarusian speakers in Poland instead of English-language desktop market (blue ocean strategy)
2. **Voice-first positioning** - Competing against Grammarly but differentiated by voice input and multi-language support
3. **Cloud-based MVP** - Prioritizing speed to market over privacy-focused on-device processing
4. **Lean validation approach** - Fake door landing page before building full product
5. **Belarusian language support** - As potential viral GTM hook (no mobile keyboards currently support it)
6. **Feature deprioritization** - Dashboard, full keyboard, and advanced activation postponed
7. **Style selection UX** - Only available during transcription, not after
8. **Direct voice activation** - Not a priority for current release
9. **Polish language added** - Now supporting Polish in addition to Russian
10. **Aggressive shipping mode** - Team dogfooding and merging without extensive review to maintain velocity

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Product & Pricing:**
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

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

**Usage Patterns:**
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

## Next Actions

**CRITICAL (Blocking launch):**
- Fix bug where dictated text fails to insert into applications
- Fix companion app connection stability issues (manual restart required)
- Implement authentication system

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Find Polish native speaker to verify localization
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets

**Product Development:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages

**Launch Preparation:**
- Build financial model and unit economics for the business
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Create schematic launch plan to review together in next call
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch

**Technical Investigation:**
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Evaluate GitBook and its free tier capabilities
- Investigate if direct keyboard voice activation is possible

**Other:**
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights