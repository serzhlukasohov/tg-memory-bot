# Startup Context
_Last updated: 2025-05-24 14:30 UTC_

## What we're building

Plyn is a mobile voice-first keyboard app targeting Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product combines voice-to-text transcription with AI-powered text beautification/enhancement, positioning as a voice-native alternative to Grammarly in underserved non-English markets.

The core value proposition is multi-language voice dictation with real-time translation capabilities and AI enhancement of spoken input for messenger and mobile communication use cases. The product uses Gemini API for audio and text processing, achieving viable unit economics at €5/month supporting ~4 hours of usage.

Key market insight: Grammarly only added Polish support in March 2026 and no competitors are actively marketing in Polish, creating a clear opportunity. Belarusian language support (not currently available on any mobile keyboards) is identified as a potential viral growth hook.

## Current Status

**Phase:** Closed beta testing via TestFlight with invitation-only access

**Current Sprint:** Aggressive shipping mode focused on core functionality over features. Team is dogfooding their own product and fixing critical stability issues before launching marketing.

**Blocking Issues:**
- Critical bug: Dictated text sometimes fails to insert
- Critical bug: Companion app frequently loses connection, requiring manual restart
- Authentication system needs implementation
- Session management for keyboard background states incomplete

**Recent Progress:**
- Translation functionality fixed and working well
- Polish language support added alongside Russian
- System prompt fixed for multilingual support
- UI polished with haptic and audio feedback
- Firebase access granted for system configuration

**Strategic Posture:** Speed to market prioritized over feature completeness. Team consciously deprioritizing dashboard, full keyboard features, and advanced activation to ship faster than potential competitors entering the Polish market.

## Key Decisions Made

1. **Market pivot to Polish-speaking users** - Shifted from English desktop voice-to-text to underserved Polish/Ukrainian/Belarusian markets in Poland (avoiding Whisperflow's $80M funded competition)

2. **Mobile-first, cloud-based MVP** - Prioritizing speed to market with cloud solution over privacy-focused on-device processing

3. **Lean validation approach** - Building fake door landing page before full product to validate demand

4. **Voice-first positioning against Grammarly** - Differentiated by voice input and multi-language emigrant support

5. **Feature deprioritization** - Dashboard, style selection post-transcription, and direct voice activation from keyboard all pushed to later phases

6. **No review merge policy** - Team moving fast enough to merge PRs without additional review cycles

7. **Critical bugs block marketing** - Explicit decision to fix stability issues before user acquisition to prevent permanent user loss

8. **Won't fix minor visual bugs** - White corners on desktop video transitions deprioritized due to planned content replacement

9. **System prompt configuration via Firebase** - Centralized prompt management for multilingual behavior

10. **2-3 week timeline to landing page launch** - Compressed schedule to beat potential market entrants

## Open Questions

**Market & Positioning:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?

**Product & UX:**
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- When should proper user research be conducted for the feature?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

**Technical & Infrastructure:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Can GitBook's free tier support the team's requirements?
- Can I update the system prompt in Firebase, and is there versioning/rollback support if the previous version needs to be restored?
- How should authentication be implemented?
- Should we set up a task board through wiki or another tool?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Unit Economics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Go-to-Market:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- What name, vibe, and emoji should be assigned to Plyn Bot?

## Next Actions

**Critical Path (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system
- Complete session management for keyboard background states

**Pre-Launch Marketing Prep:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Replace the video on the website
- Find Polish native speaker to verify localization

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Business Model & Economics:**
- Build financial model and unit economics for the business
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Product Development:**
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Test which AI model performs best for Polish language generation
- Merge the pending pull requests
- Test the updated system prompt across all languages
- Test translation feature with Belarusian and Russian languages
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Update system prompt in Firebase
- Add serzh to TestFlight
- Evaluate GitBook and its free tier capabilities

**Technical Research:**
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Investigate if direct keyboard voice activation is possible
- Check how Whisper Flow handles session management and keyboard background behavior

**Go-to-Market Strategy:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Create schematic launch plan to review together in next call
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch

**Project Management:**
- Set up a task board system (possibly through wiki)
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Provide bot configuration (name/vibe/emoji) or review suggested options

**Learning & Networking:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights