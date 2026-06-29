# Startup Context
_Last updated: 2024-12-20 10:30 UTC_

## What we're building
Plyn is a mobile-first AI voice keyboard targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines real-time voice transcription with AI beautification/enhancement, positioning as a voice-first alternative to Grammarly. Core differentiation: multi-language support for emigrant communities (including Belarusian - currently unsupported by any mobile keyboard), superior translation quality versus Google, and voice-as-primary-input UX. Using Gemini API for audio and text processing with cloud-based architecture prioritizing speed to market over on-device privacy. Unit economics: €5/month supports ~4 hours usage with viable margins (€0.53 costs in April 2026 testing).

## Current Status
**Phase**: Closed beta (TestFlight) → Landing page validation  
**Priority**: Aggressive shipping mode - core voice input functionality only, deprioritizing dashboard, full keyboard features, and advanced activation. Team is dogfooding the product daily.

**Recent wins**: 
- Multilingual support fixed (Polish + Russian working)
- Translation quality superior to Google
- UI polish complete (haptics, audio feedback)
- System prompt stabilized across languages

**Blockers**: 
- Authentication not implemented (Firebase access granted but not configured)
- Performance issues with gemini-2.5-flash model

**Go-to-market**: Lean validation with fake door landing page planned for 2-3 week launch. Target 100 Ukrainian/Belarusian beta users initially. Market opportunity: Grammarly only added Polish in March 2026, no competitors marketing in Polish.

## Key Decisions Made
1. **Market pivot**: English desktop voice-to-text → Polish/Ukrainian/Belarusian mobile keyboard (blue ocean vs Whisperflow's $80M saturated market)
2. **Cloud-first architecture**: Prioritize speed to market over on-device privacy for non-technical users
3. **Voice-first positioning**: Compete against Grammarly but differentiated by voice input as primary UX
4. **Belarusian support**: Use unique language support as viral GTM hook
5. **Lean validation approach**: Fake door landing page before full product build
6. **Aggressive descoping**: Dashboard, full keyboard, advanced activation deprioritized for speed
7. **Style selection UX**: Only available during transcription, not after
8. **No direct voice activation**: Competitor-style keyboard activation not priority
9. **AI agent for team knowledge**: Shared knowledge base in chat to track decisions
10. **TestFlight for closed beta**: Controlled access with invitation codes

## Open Questions

**Market & Pricing**:
- What is Grammarly's penetration in Polish market and are they actively advertising?
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for similar subscriptions?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- Is there a blocker preventing competitors from entering Polish market?
- What usage limits do competitors have on subscription plans?
- Is there open analytics on monthly minutes users need?

**Product & Technical**:
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- Which AI model performs best for Polish language?
- Do existing voice-to-text solutions actually target Polish/Ukrainian/Russian markets?
- Which models (Whisper v3, Gemini) work well with target languages?
- Is it technically possible to access conversation context from custom mobile keyboard?
- How popular are voice messages in messengers and what's demand for transcription?
- Can on-device models like Gemini's local version work for non-English languages?
- Can GitBook's free tier support team requirements?
- Is current model same as previously used? Why is system running slowly?
- Can system prompt be updated in Firebase with versioning/rollback support?
- How should authentication be implemented?

**GTM**:
- Can we find underserved niche/use case for emigrants who don't know local language?
- How to properly record demo video - with hands or screencast only?

## Next Actions

**Research & Validation**:
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research pricing - what target users typically pay for subscription products
- Find Polish native speaker to verify localization
- Test which AI model performs best for Polish language generation
- Ask friend launching text-to-speech startup about market insights
- Perform competitor analysis of Wispr Flow, VoiceInk, others (value props, features, marketing, pricing)
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support/target Polish/Ukrainian/Russian markets
- Test Whisper v3 and Gemini model performance with target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and transcription demand in WhatsApp, Telegram, other messengers
- Evaluate GitBook and free tier capabilities

**Financial Modeling**:
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Product & Technical**:
- Implement authentication system
- Debug and fix performance issues with gemini-2.5-flash model
- Update system prompt in Firebase
- Rebuild/redraw APK after adding Polish language
- Test haptic vibration feedback on actual device
- Add serzh to TestFlight

**Landing Page & GTM**:
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Create schematic launch plan to review together
- Schedule sync call to create timeline and roadmap for 2-3 week sprint to launch

**Process**:
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits