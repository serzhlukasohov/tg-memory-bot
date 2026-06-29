# Startup Context
_Last updated: 2024-12-19 14:30 UTC_

## What we're building
Plyn is a voice-first AI keyboard for mobile devices targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines real-time voice dictation with AI-powered text enhancement ("beautification") and translation capabilities across multiple languages. Unlike competitors like Grammarly (which only added Polish support in March 2026), Plyn focuses on voice-first input for non-English markets, specifically targeting emigrant communities who need multilingual communication tools. The product uses Gemini API for audio and text processing, with superior translation quality compared to Google Translate. Current unit economics show €5/month can support ~4 hours of usage with viable margins.

## Current Status
**Phase:** Pre-launch debugging and stabilization
**Distribution:** Closed TestFlight beta with invitation codes
**Tech Stack:** Cloud-based MVP using gemini-2.5-flash model, Firebase backend
**Languages Supported:** Polish, Russian, Belarusian (with translation between them)

**Critical Blockers:**
- Text insertion failures during dictation
- Companion app connection issues requiring manual restarts
- Session management for background states (calls, interruptions)
- Missing authentication system

**Recent Progress:**
- Multilingual support fixed in system prompt
- UI polish with haptic and audio feedback implemented
- Translation functionality working well
- Team actively dogfooding the product

**Strategic Priority:** Speed to market over feature completeness - deliberately deprioritizing dashboard, full keyboard features, and advanced activation to focus on core voice input functionality. Critical bugs must be fixed before any marketing/user acquisition.

## Key Decisions Made
1. **Market Positioning:** Pivot from English-language desktop voice-to-text to mobile-first keyboard for underserved Polish/Ukrainian/Belarusian markets (blue ocean strategy vs competing with Whisperflow's $80M funding)
2. **Target Audience:** Polish, Ukrainian, and Belarusian language speakers in Poland, with Belarusian support as potential viral hook (no mobile keyboards currently support it)
3. **Core Differentiation:** Voice-first input + AI beautification layer, positioning against Grammarly but with multilingual emigrant focus
4. **Go-to-Market:** Lean validation with fake door landing page before full product build (2-3 week timeline)
5. **Technology Approach:** Cloud-based MVP prioritizing speed over privacy-focused on-device processing
6. **Feature Scope:** Deprioritize dashboard, style selection post-transcription, and direct voice activation from keyboard
7. **Quality Gate:** Fix critical bugs before user acquisition - launching broken will cause permanent user loss
8. **Development Process:** Moving from ad-hoc conversations to structured task tracking via board/wiki system
9. **Language Implementation:** System prompt fixed to work correctly across all languages; Polish and Russian fully supported
10. **UI/UX:** Added haptic vibration and sound effects on paste/insert actions; team dogfooding own keyboard

## Open Questions

**Market & Pricing:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- Is there any blocker preventing competitors from entering the Polish market?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Product & Technical:**
- How to properly record demo video - with hands or just screencast?
- Which AI model performs best for Polish language - likely Google/Gemini?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How should session management handle edge cases like incoming calls during active sessions?

**Use Cases & Positioning:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?

**Infrastructure:**
- Can GitBook's free tier support the team's requirements?
- Can system prompts be updated in Firebase with versioning/rollback support?

## Next Actions

**CRITICAL (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system
- Resolve session management for keyboard background states (study Whisper Flow reference implementation)

**Pre-Launch Marketing Prep:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets

**Product Development:**
- Test translation feature with Belarusian and Russian languages
- Test haptic vibration feedback on actual device
- Test the updated system prompt across all languages
- Merge the pending pull requests (after critical bugs fixed)
- Evaluate GitBook and its free tier capabilities

**Business Planning:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together in next call
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well

**Product Validation:**
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Process & Infrastructure:**
- Set up a task board system (possibly through wiki)
- Set up shared AI agent with knowledge base in chat to track all decisions and research

**Knowledge Gathering:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights