# Startup Context
_Last updated: 2024-12-19 18:45 UTC_

## What we're building

Plyn is an AI-powered voice-to-text keyboard with intelligent text beautification targeting Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product combines real-time voice dictation with AI enhancement and translation capabilities, positioning as a "better Grammarly" alternative differentiated by voice-first input and multi-language support for emigrant communities.

The product uses Gemini 2.5 Flash for processing, currently supports Polish and Russian languages with translation between them, and is in closed TestFlight beta. Unit economics show €5/month can support ~4 hours of usage with viable margins using cloud-based processing (€0.53 monthly costs in early testing).

Key differentiation: Belarusian language support (no mobile keyboards currently offer this), superior translation quality compared to Google Translate, and focus on underserved non-English markets ignored by well-funded competitors like Whisperflow.

## Current Status

**Phase:** Pre-launch validation - preparing fake door landing page for demand testing

**Technical Status:** 
- Closed beta on TestFlight with invitation-only access
- Polish and Russian language support implemented
- Performance issues identified with current gemini-2.5-flash configuration requiring troubleshooting
- Translation behavior inconsistent (auto-translates unpredictably) - needs prompt engineering

**Go-to-Market:**
- Domain: plyn.io
- Target: 2-3 week sprint to landing page launch
- Market gap confirmed: Grammarly only added Polish in March 2026, no competitors actively marketing in Polish
- Landing page development in progress at plyn-site.vercel.app

**Team Infrastructure:** Exploring GitBook for shared knowledge base as part of AI-first startup approach

## Key Decisions Made

1. **Market Focus:** Target Polish, Ukrainian, Russian, and Belarusian speakers in Poland (not English-speaking desktop users)
2. **Product Strategy:** Voice-first keyboard with AI beautification layer, not generic transcription commodity
3. **Go-to-Market:** Launch fake door landing page (plyn.io) before building full product to validate demand
4. **Positioning:** "Better Grammarly" competitor differentiated by voice input and multi-language support
5. **Technology Stack:** Cloud-based MVP using Gemini 2.5 Flash (not on-device processing) prioritizing speed to market
6. **Belarusian Support:** Use as viral hook since no mobile keyboards currently support it
7. **Branding:** Use green color from holas.ai for beta phase
8. **Pricing Model:** €5/month supporting ~4 hours usage (exact minutes still being validated)
9. **Mobile-First:** Focus on everyday communication scenarios (messengers, smart keyboard) not desktop/developer tools
10. **AI-First Operations:** Build shared knowledge base with agent in chat to track decisions and research

## Open Questions

**Market & Competition:**
- What is Grammarly's actual penetration and advertising activity in Polish market?
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for subscription products?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?

**Product & Technical:**
- Why does language detection/translation work inconsistently (sometimes auto-translates, sometimes not)?
- Why is the system experiencing performance issues with gemini-2.5-flash - has configuration changed?
- Which AI model performs best for Polish language?
- How do Whisper v3 vs Gemini compare for target languages?
- Is it technically possible to access conversation context from within custom mobile keyboard?
- Can on-device models work effectively for non-English languages?

**Business Model:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on subscription plans?
- Is there open analytics on typical user monthly usage patterns?

**Landing Page:**
- Should pricing be displayed on waitlist page?
- How to record demo video - with hands or just screencast?

**Team Tools:**
- Can GitBook's free tier support team requirements?

## Next Actions

**Critical Path (Landing Page Launch):**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing keyboard in action
- Set up email collection worker for waitlist
- Find Polish native speaker to verify localization
- Buy plyn.pl domain (research GoDaddy broker acquisition ~$70)

**Product & Technical:**
- Troubleshoot performance issues with gemini-2.5-flash configuration
- Debug system prompt to fix inconsistent language detection/translation behavior
- Rebuild/redraw APK after Polish language additions
- Test which AI model performs best for Polish language generation
- Test Whisper v3 vs Gemini model performance with all target languages
- Calculate cost per hour of text based on token usage, verify counting methodology

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm competition gap
- Research pricing Polish/Ukrainian/Belarusian users pay for subscriptions
- Research where to find target audience (Telegram expat groups, Facebook groups Warsaw/Wroclaw)
- Perform competitor analysis: Wispr Flow, VoiceInk - features, marketing, pricing, subscription limits
- Find open analytics on user monthly usage patterns
- Analyze voice message usage and transcription demand in WhatsApp, Telegram, messengers

**Strategic Planning:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Build financial model and unit economics
- Create schematic launch plan for review
- Schedule sync call to create timeline and roadmap
- Set up shared AI agent with knowledge base in chat

**Team:**
- Evaluate GitBook and free tier capabilities
- Add serzh to TestFlight (if not completed)
- Watch JTBD (Jobs-to-be-Done) video tutorial

**Network:**
- Ask friend launching text-to-speech startup about market insights

**Technical Research:**
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard