# Startup Context
_Last updated: 2024-01-09 14:30 UTC_

## What we're building

Plyn is a voice-first AI keyboard for mobile targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines voice dictation with AI-powered text enhancement ("beautification"), positioning against Grammarly but differentiated by voice-first input and multi-language support for emigrant communities. The keyboard transcribes speech in real-time and can translate between languages, with translation quality superior to Google Translate. Currently in closed TestFlight beta, the product uses Gemini API (gemini-2.5-flash) for audio and text processing at minimal costs (~€0.53/month in testing, €5/month target supporting ~4 hours usage).

Key market insight: Grammarly only added Polish support in March 2026 with no competitors actively marketing in Polish. Belarusian language support (currently unsupported by any mobile keyboard) identified as potential viral go-to-market hook.

## Current Status

**Phase:** Closed beta testing and bug fixing before marketing launch

**Current Priority:** Fix critical stability issues blocking user research and acquisition
- Dictated text sometimes fails to insert into target applications
- Companion app frequently loses connection requiring manual restarts

**Recent Progress:**
- Translation functionality working well across Polish, Russian, and Belarusian
- UI polish complete with haptic and audio feedback on paste/insert
- Multilingual system prompt fixed
- Team actively dogfooding the product
- Authentication identified as missing but not yet implemented

**Approach:** Aggressive shipping mode - deprioritizing features (dashboard, full keyboard, advanced activation) to focus on core voice input functionality. Planning fake door landing page validation before full product launch (2-3 week timeline).

## Key Decisions Made

1. **Market positioning:** Target Polish/Ukrainian/Belarusian speakers in Poland rather than compete in saturated English-language market
2. **Cloud-first architecture:** Prioritizing speed to market with cloud-based MVP over privacy-focused on-device processing
3. **Voice-first differentiation:** Position against Grammarly but lead with voice input as primary interface
4. **Lean validation approach:** Launch fake door landing page before building full product
5. **Critical bugs before marketing:** Must fix stability issues before user acquisition to prevent permanent user loss
6. **Feature deprioritization:** Dashboard, style selection post-transcription, and direct voice activation not priorities
7. **System prompt fixes:** Multilingual support fixed and deployed
8. **Team dogfooding:** Using own voice keyboard for testing
9. **Sound/haptic feedback:** Added to paste/insert actions for better UX
10. **Visual bug triage:** Not fixing minor desktop website video transition issues due to planned content replacement

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Product & Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- How should authentication be implemented?
- Can system prompts be versioned/rolled back in Firebase?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Go-to-Market:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

**Unit Economics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Tooling:**
- Can GitBook's free tier support the team's requirements?
- Should we set up a task board through wiki or another tool?

## Next Actions

**CRITICAL (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system

**Pre-Launch Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages

**Landing Page & Marketing:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Create schematic launch plan to review together in next call

**Product Development:**
- Add serzh to TestFlight
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages
- Merge the pending pull requests
- Investigate if direct keyboard voice activation is possible
- Check how Whisper Flow handles session management and keyboard background behavior
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Business & Planning:**
- Build financial model and unit economics for the business
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Set up a task board system (possibly through wiki)

**Learning & Research:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Evaluate GitBook and its free tier capabilities