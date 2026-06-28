# Startup Context
_Last updated: 2024-12-19 14:30 UTC_

## What we're building
Plyn is an AI-powered voice-to-text keyboard with text beautification targeting Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product differentiates from competitors like Grammarly through voice-first input and multi-language support for emigrant communities. The core value proposition is helping users speak in their native language and receive AI-enhanced, polished text output. The product is mobile-first, cloud-based, and targeting non-technical users who value convenience over privacy. Belarusian language support serves as a potential viral hook since no mobile keyboards currently support it.

## Current Status
- **Phase**: Pre-launch validation and early product development
- **Product**: In closed TestFlight beta with invitation-code access
- **Go-to-market**: Building fake door landing page on plyn-site.vercel.app to validate demand before full build
- **Timeline**: 2-3 week sprint target to landing page launch
- **Market opportunity**: Grammarly only added Polish support in March 2026; no active Polish-language marketing from competitors
- **Unit economics**: €5/month supports ~4 hours usage with viable margins using Gemini API
- **Team tooling**: Evaluating GitBook for documentation and knowledge management

## Key Decisions Made
- **2026-Q2**: Target Polish, Ukrainian, Russian, and Belarusian speakers in Poland as primary market
- **2026-Q2**: Build voice-first keyboard with AI beautification layer, positioning as "better Grammarly"
- **2026-Q2**: Target non-technical users rather than programmers
- **2026-Q2**: Start with cloud-based MVP prioritizing speed over on-device privacy
- **2026-Q2**: Launch fake door landing page (plyn.io) to validate demand before building full product
- **2026-Q2**: Use Gemini 2.5 Flash for Belarusian language support
- **2026-Q2**: Use green color from holas.ai for beta branding
- **2026-Q2**: Build AI-first startup with shared knowledge base and agent to track decisions
- **Recent**: Add serzh to TestFlight for product access
- **Recent**: Evaluate GitBook for team documentation

## Open Questions
**Market & Competition**
- What is Grammarly's penetration in Polish market and are they actively advertising?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- What usage limits do competitors have on subscription plans?
- Is there open analytics on typical user monthly usage patterns?

**Pricing & Economics**
- What average price point do Polish/Ukrainian/Belarusian users in Poland pay for subscriptions?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Product & Technical**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Can GitBook's free tier support team requirements?

**Go-to-Market**
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on waitlist landing page?
- How to record demo video - with hands or just screencast?
- How popular are voice messages in messengers and what's demand for voice-to-text?
- Can we find underserved niche or use case (e.g., emigrants who don't know local language)?

## Next Actions
**Market Research**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users typically pay for subscriptions
- Perform competitor analysis of Wispr Flow, VoiceInk, others - analyze value propositions, features, marketing, pricing
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors support and target Polish, Ukrainian, Russian markets
- Find open analytics on typical user monthly usage patterns
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, other messengers
- Ask friend launching text-to-speech startup about market insights

**Product Development**
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for landing page waitlist
- Record real demo video on actual device showing keyboard in action
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard

**Operations & Planning**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Create schematic launch plan to review together in next call
- Schedule sync call to create timeline and roadmap - 2-3 week sprint to landing page launch
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Evaluate GitBook and its free tier capabilities
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits