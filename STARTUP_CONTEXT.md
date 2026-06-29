# Startup Context
_Last updated: 2024-12-20 18:45 UTC_

## What we're building

Plyn is a voice-first AI keyboard for mobile that transcribes, translates, and beautifies spoken input across Polish, Ukrainian, Russian, and Belarusian languages. The product targets emigrants in Poland (particularly Ukrainian and Belarusian speakers) who need multilingual communication support that existing solutions don't provide.

The core differentiation is voice-first input combined with AI enhancement (grammar, style, tone adjustment) and real-time translation—positioning against Grammarly but serving underserved non-English markets. Belarusian language support is a unique feature with viral potential, as no mobile keyboards currently support it.

The product is cloud-based MVP using Gemini API, prioritizing speed to market over privacy-focused on-device processing. Unit economics show €5/month can support ~4 hours of usage with viable margins.

## Current Status

**Phase:** Private TestFlight beta, pre-launch  
**Priority:** Fix critical bugs blocking user retention before any marketing efforts

**Recent progress:**
- Translation and multilingual support fixed and working well
- UI polished with haptic and audio feedback
- Team dogfooding the product
- Plyn Bot (OpenClaw agent) initialized for project context and task management

**Critical blockers:**
- Dictated text sometimes fails to insert
- Companion app frequently loses connection, requiring manual restart
- Authentication system not yet implemented
- Task tracking system needs structure (moving to board/wiki)

**Competitive pressure:** High awareness that competitors could enter Polish market; emphasizing speed to market over feature completeness.

## Key Decisions Made

1. **Target market pivot** - Focus on Polish/Ukrainian/Belarusian emigrants in Poland rather than English-language desktop market (blue ocean strategy)
2. **Voice-first mobile** - Build mobile keyboard with voice input, not desktop or developer tools
3. **Cloud-based MVP** - Use Gemini API rather than on-device processing for faster launch
4. **Lean validation** - Launch fake door landing page before building full product
5. **Language support** - Polish, Ukrainian, Russian, Belarusian (Belarusian as viral hook)
6. **No user acquisition until bugs fixed** - Critical bugs must be resolved before marketing to prevent permanent user loss
7. **Feature deprioritization** - Dashboard, full keyboard features, direct voice activation deferred; focus on core voice input
8. **Style selection timing** - Only available during transcription, not after
9. **Merge without review** - Ship pull requests quickly without additional review cycles
10. **Don't fix desktop video bug** - White corners during video transitions not worth fixing since video will be replaced

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in Polish market and are they actively advertising?
- Is there any blocker preventing competitors from entering Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, Russian markets?
- Where to buy traffic - Instagram, Facebook, TikTok, or other channels?

**Pricing & Economics:**
- What price point do Polish/Ukrainian/Belarusian users in Poland pay for subscription products?
- Should pricing be displayed on waitlist landing page?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on subscription plans?
- Is there open analytics on typical user monthly usage?

**Product & Technical:**
- Which AI model performs best for Polish language?
- Which models (Whisper v3, Gemini) work well with target languages?
- Is it technically possible to access conversation context from custom keyboard on mobile?
- How popular are voice messages in messengers and what's demand for voice-to-text?
- Can on-device models work effectively for non-English languages?
- Is it technically feasible to implement direct voice activation from keyboard?
- Is there actual latency delay when changing styles after dictation?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Tools & Operations:**
- Can GitBook's free tier support team requirements?
- Should task board be set up through wiki or another tool?
- What name, vibe, and emoji should be assigned to Plyn Bot?
- Can Plyn Bot read and respond in Cyrillic/non-English languages?

**Go-to-Market:**
- Can we find an underserved niche (e.g., emigrants who don't know local language)?
- How to record demo video - with hands or just screencast?
- Where to find and engage target audience?
- When should proper user research be conducted?

## Next Actions

**Critical (blocking launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system
- Set up task board system (possibly through wiki)

**Pre-launch preparation:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing keyboard in action
- Set up email collection worker for landing page waitlist
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Replace the video on the website

**Market research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries
- Research pricing - what Polish/Ukrainian/Belarusian users pay for subscriptions
- Perform competitor analysis of Wispr Flow, VoiceInk, others (value props, features, marketing, pricing)
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors support Polish, Ukrainian, Russian markets
- Research where to find target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Analyze voice message usage patterns in WhatsApp, Telegram, other messengers

**Product development:**
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Test haptic vibration feedback on actual device
- Test the updated system prompt across all languages
- Check how Whisper Flow handles session management and keyboard background behavior

**Planning & operations:**
- Build financial model and unit economics for the business
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Create schematic launch plan to review together
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Provide bot configuration (name/vibe/emoji) or review suggested options
- Evaluate GitBook and its free tier capabilities

**Nice to have:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights