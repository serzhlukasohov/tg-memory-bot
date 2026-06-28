# Startup Context
_Last updated: 2024-12-19 14:30 UTC_

## What we're building
Plyn is an AI-powered voice keyboard for mobile targeting Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product combines real-time voice dictation with AI text beautification and translation capabilities, positioning as a "better Grammarly" alternative differentiated by voice-first input and multi-language support for emigrant communities. Key features include voice-to-text transcription, AI enhancement of spoken input, and real-time translation between supported languages. Translation quality has proven superior to Google Translate. The product uses Gemini API for audio and text processing with unit economics of €5/month supporting ~4 hours of usage.

## Current Status
**Phase:** Closed beta testing via TestFlight with invitation-only access

**Recent Progress:**
- Polish language support added to the product
- Real-time voice dictation and translation working between Polish and Russian
- Identified translation consistency issues requiring prompt engineering fixes
- Team member (serzh) being onboarded to TestFlight for product testing

**Current Focus:**
- Stabilizing translation behavior through prompt engineering
- Pre-launch validation via fake door landing page (plyn.io) before full build
- Targeting 2-3 week sprint to landing page launch
- Market opportunity window: Grammarly only added Polish in March 2026, no active Polish-market competitors identified

**Strategic Positioning:**
- Blue ocean strategy in underserved non-English markets vs. saturated English desktop market
- Belarusian language support as viral GTM hook (no mobile keyboards currently support it)
- Mobile-first, cloud-based MVP prioritizing speed over on-device privacy

## Key Decisions Made
1. **Market pivot** - Target Polish/Ukrainian/Russian/Belarusian speakers in Poland vs. English-speaking market
2. **Product focus** - Voice-first AI keyboard with beautification layer vs. general voice-to-text or developer tools
3. **Launch strategy** - Fake door landing page (plyn.io) for demand validation before full product build
4. **Competitive positioning** - Position as "better Grammarly" with voice-first and multi-language differentiation
5. **Language support** - Polish, Ukrainian, Russian, and Belarusian with Gemini 2.5 Flash for Belarusian
6. **Branding** - Use green color from holas.ai for beta phase
7. **Technical architecture** - Cloud-based MVP using Gemini API vs. on-device processing
8. **Target timeline** - 2-3 week sprint to landing page launch to move before competitors
9. **Team infrastructure** - AI-first approach with shared knowledge base and GitBook evaluation
10. **Distribution** - TestFlight for closed beta with controlled access via invitation codes

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively advertising?
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for subscription products?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics on typical user monthly usage patterns?

**Product & Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within custom mobile keyboard?
- Can on-device models like Gemini's local version work for non-English languages?
- How popular are voice messages in messengers and what's demand for voice-to-text conversion?

**Economics & Metrics:**
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Go-to-Market:**
- Should pricing be displayed on waitlist landing page?
- How to record demo video - with hands or just screencast?
- Can we find underserved niche/use case for emigrants who don't know local language?
- Can GitBook's free tier support team requirements?

## Next Actions

**Landing Page & Launch (Priority):**
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for waitlist
- Record real demo video on actual device showing keyboard in action
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Schedule sync call to create timeline and roadmap for 2-3 week sprint

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard queries to confirm lack of competition
- Research pricing - what target users typically pay for subscription products
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Ask friend launching text-to-speech startup about market insights

**Product Development:**
- Fix translation consistency issues through prompt engineering
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well

**Competitive Intelligence:**
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - value propositions, features, marketing, pricing
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors support and target Polish/Ukrainian/Russian markets
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, other messengers

**Business Model:**
- Build financial model and unit economics
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Team & Infrastructure:**
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Evaluate GitBook and its free tier capabilities
- Create schematic launch plan to review in next call
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits