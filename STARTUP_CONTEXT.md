# Startup Context
_Last updated: 2025-01-25 14:30 UTC_

## What we're building

Plyn is a mobile-first AI voice keyboard targeting Polish, Ukrainian, Russian, and Belarusian speakers in Poland. The app provides voice-to-text dictation with AI enhancement (beautification/translation) for everyday communication in messengers and other apps. The core differentiator is multilingual support for emigrant communities who need seamless switching between languages, plus Belarusian language support (currently unavailable on any mobile keyboard).

The product uses cloud-based processing (Gemini API) with a companion app architecture. Unit economics show €5/month can support ~4 hours of usage with viable margins. Current costs are minimal (€0.53 in April 2026).

We're competing in a blue ocean - Grammarly only added Polish support in March 2026, and no competitors actively market Polish-language voice keyboard solutions. We're taking a mobile-first, non-English market approach rather than competing in the saturated English desktop market.

## Current Status

**Phase**: Pre-launch preparation - app nearly complete, website deployed, pausing before marketing validation decisions.

**Recently Completed**:
- Website deployed to plyn.click
- Translation functionality fixed with superior quality to Google Translate
- Polish language support added alongside Russian
- Multilingual support fixed in system prompt
- Domain secured (plin.click as placeholder, plyn.click as public site)

**Current Priorities**:
1. Marketing strategy decision: simple email collection vs. paid pre-orders (pending expert consultation)
2. Implement response styles feature (last major feature before launch readiness)
3. Create product demo video
4. ASO/ASA mentor call with Yan to understand cost structure (~$200/geo)

**Blocking Issues**: None critical - team deliberately pausing to consult marketing experts before choosing validation approach.

**Team is dogfooding**: Using their own voice keyboard in daily work.

## Key Decisions Made

1. **Target Polish/Ukrainian/Russian/Belarusian speakers in Poland** - pivoted from English desktop market to underserved non-English mobile market
2. **Mobile-first voice keyboard with AI beautification** - positioned against Grammarly but voice-first and multilingual
3. **Cloud-based MVP over on-device processing** - prioritizing speed to market for non-technical users
4. **Belarusian language as viral hook** - no mobile keyboards currently support it
5. **Speed over features** - aggressively shipping core functionality, deprioritizing dashboard, full keyboard, advanced activation
6. **Critical bugs must be fixed before user acquisition** - will cause permanent user loss if launched broken
7. **Not fixing minor visual bugs when content is changing anyway** - pragmatic prioritization (e.g., white corners on video)
8. **Domain strategy**: plyn.click as public domain, plinklink.com (€9.05) as placeholder
9. **Pause email capture pending marketing strategy decision** - avoiding premature commitment to validation approach
10. **Merge PRs without additional review** - maintaining development velocity

## Open Questions

**Market & Competition**:
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?

**Pricing & Business Model**:
- What average price do Polish/Ukrainian/Belarusian users in Poland pay for similar subscriptions?
- Should pricing be displayed on the waitlist landing page?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on typical monthly usage minutes?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - per country or more granular?

**Technical & Product**:
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Unit Economics**:
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Go-to-Market Strategy**:
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?
- How to record demo video - with hands or just screencast?
- How popular are voice messages in different messengers and what's demand for voice-to-text conversion?

**Tooling**:
- Can GitBook's free tier support the team's requirements?
- Should we set up a task board through wiki or another tool?

**Bot Configuration**:
- What name, vibe, and emoji should be assigned to Plyn Bot?
- Can Plyn Bot read and respond to messages in Cyrillic/non-English languages?

## Next Actions

**Marketing & Launch**:
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Record real demo video on actual device showing the keyboard in action
- Research where to find and engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Schedule ASO/ASA mentor call with Yan
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Create product demo video
- Set up email collection worker for landing page waitlist (paused pending strategy decision)

**Product Development**:
- Implement response styles (warm, friendly, etc.) in the app
- Implement authentication system
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation

**Research & Analysis**:
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Build financial model and unit economics for the business
- Find Polish native speaker to verify localization
- Test which AI model performs best for Polish language generation
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Ask friend launching text-to-speech startup about market insights

**Planning & Organization**:
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Create schematic launch plan to review together in next call
- Set up a task board system (possibly through wiki)
- Finalize mountain route; share elevation profile with Yan

**Technical Tasks**:
- Evaluate GitBook and its free tier capabilities
- Set up Cloudflare Pages CI for website
- Provide bot configuration (name/vibe/emoji) or review suggested options

**Learning**:
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits