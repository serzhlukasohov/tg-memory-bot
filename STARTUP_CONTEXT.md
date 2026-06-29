# Startup Context
_Last updated: 2024-01-09_

## What we're building
Plyn is a voice-first AI keyboard for mobile devices targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines real-time voice dictation with AI text enhancement (beautification layer) and translation capabilities across multiple languages. The core differentiation is voice-first input with multi-language support for emigrant communities, positioning against Grammarly (which only added Polish support in March 2026) but with superior translation quality and voice interface. The product uses Gemini API for audio and text processing with a cloud-based architecture prioritizing speed to market over on-device privacy.

## Current Status
**Phase:** Pre-launch closed testing (TestFlight)
**Priority:** Fixing critical bugs before user acquisition

The team is in aggressive shipping mode, consciously deprioritizing non-essential features (dashboard, full keyboard, advanced activation) to focus on core voice input functionality. Two critical bugs are blocking launch:
1. Dictated text sometimes fails to insert
2. Companion app loses connection requiring manual restarts

Polish and Russian language support are implemented with working translation. UI polish complete with haptic and audio feedback. Authentication identified as critical missing piece. The team is dogfooding their own product and has identified a clear market opportunity with no active Polish-language competitors.

Plyn Bot has been brought online for testing but setup remains incomplete.

## Key Decisions Made
1. **Market pivot to Polish/Ukrainian/Belarusian speakers in Poland** - abandoned saturated English desktop market for underserved non-English mobile opportunity
2. **Voice-first positioning with AI beautification** - differentiating from commodity transcription through enhancement layer
3. **Cloud-based MVP over on-device processing** - prioritizing speed to market and targeting non-technical users
4. **Lean validation with fake door landing page** - compressed 2-3 week timeline before building full product
5. **Belarusian language as viral hook** - no mobile keyboards currently support it
6. **Critical bugs must be fixed before user acquisition** - recognized users lost to bugs won't return
7. **Aggressive feature deprioritization** - dashboard, style-after-transcription, direct voice activation all postponed
8. **System prompt fixed for multilingual support** - consistent language handling across all supported languages
9. **Team dogfooding the product** - using voice keyboard themselves for testing
10. **Merge without additional review** - moving quickly on stable PRs

## Open Questions

**Market & Positioning:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?

**User Acquisition:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Where to find and engage target audience - which Telegram/Facebook expat groups?

**Technical & Product:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?
- Should we set up a task board through wiki or another tool?
- Can GitBook's free tier support the team's requirements?

**Economics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Use Cases:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

## Next Actions

**Critical (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system

**Pre-Launch Essential:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Replace the video on the website
- Find Polish native speaker to verify localization

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products

**Product Development:**
- Add serzh to TestFlight
- Test the updated system prompt across all languages
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Merge the pending pull requests
- Test translation feature with Belarusian and Russian languages
- Update system prompt in Firebase

**Technical Research:**
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Check how Whisper Flow handles session management and keyboard background behavior
- Investigate if direct keyboard voice activation is possible
- Evaluate GitBook and its free tier capabilities

**Planning & Strategy:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Create schematic launch plan to review together in next call
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Set up a task board system (possibly through wiki)
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well

**Domain & Infrastructure:**
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)

**User Research:**
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Find open analytics on typical user monthly usage patterns

**Learning:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights