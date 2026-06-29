# Startup Context
_Last updated: 2024-01-09 14:30 UTC_

## What we're building

Plyn is a mobile-first AI voice keyboard for Polish, Ukrainian, Russian, and Belarusian speakers in Poland. The product combines real-time voice transcription with AI beautification and translation capabilities, positioning as a voice-first alternative to Grammarly with multi-language support for emigrant communities.

The core value proposition: speak naturally in any supported language, and the keyboard transcribes, enhances, and optionally translates your message before inserting it into any app. Built on Gemini API for superior translation quality compared to Google Translate, with a focus on the underserved Polish market where Grammarly only added support in March 2026.

Unit economics: €5/month supports ~4 hours of usage with viable margins. Current tech stack uses Gemini 2.5 Flash for audio and text processing.

## Current Status

**Phase:** Pre-launch marketing preparation

**Live infrastructure:**
- Public website deployed at plin.click
- TestFlight closed beta with invitation codes
- Firebase backend configured
- Product feature-complete except response styles

**Immediate priorities:**
1. Marketing strategy validation (consulting experts on ASO/ASA vs email capture vs pre-orders)
2. Demo video creation for marketing materials
3. Response styles implementation (final feature before launch)

**Recent milestones:**
- Website successfully deployed to production domain
- Translation functionality fixed and working well
- Multi-language support stable in system prompt
- UI polish complete (haptic/audio feedback)

**Known blockers:**
- Marketing approach undecided (paused pending expert consultation)
- ASO/ASA cost structure unclear (~$200/geo needs definition)
- Critical bugs recently fixed but stability monitoring ongoing

## Key Decisions Made

1. **Market positioning pivot** - Target Polish/Ukrainian/Russian/Belarusian speakers in Poland instead of competing in saturated English desktop market (blue ocean strategy)

2. **Mobile-first, cloud-based MVP** - Prioritize speed to market over privacy-focused on-device processing, targeting non-technical users

3. **Voice-first differentiation** - Position against Grammarly but differentiated by voice input and multi-language support for emigrants

4. **Belarusian as viral hook** - Include Belarusian language support (no existing mobile keyboards support it) as potential go-to-market differentiator

5. **Aggressive shipping focus** - Deprioritize dashboard, full keyboard, advanced activation features to ship core voice input functionality faster

6. **Bug-first launch philosophy** - Critical bugs must be fixed before user acquisition to prevent permanent user loss

7. **Domain strategy** - Acquired plin.click as primary domain; plinklink.com as placeholder (€9.05 via Cloudflare)

8. **Style selection UX** - Only available during transcription, not after completion

9. **Marketing validation pause** - Deliberately pausing email capture to consult experts before choosing between simple collection vs complex paid pre-orders

10. **Website deployment** - Published to plin.click domain as production site

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Pricing & Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?

**Go-to-Market:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?

**Product & Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**User Research:**
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- When should proper user research be conducted for the feature?

**Tools & Infrastructure:**
- Can GitBook's free tier support the team's requirements?
- Can I update the system prompt in Firebase, and is there versioning/rollback support if the previous version needs to be restored?
- Should we set up a task board through wiki or another tool?

**Demo & Marketing:**
- How to properly record demo video - with hands or just screencast?

## Next Actions

**Marketing & Launch (High Priority):**
- Schedule ASO/ASA mentor call with Yan
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Create product demo video
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw

**Product Development:**
- Implement response styles (warm, friendly, etc.) in the app
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages

**Research & Planning:**
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Build financial model and unit economics for the business
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Create schematic launch plan to review together in next call
- Review competitor subscription limits and pricing tiers

**Technical Investigation:**
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Test which AI model performs best for Polish language generation
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Investigate if direct keyboard voice activation is possible

**Localization & Testing:**
- Find Polish native speaker to verify localization
- Add serzh to TestFlight

**Infrastructure & Tools:**
- Evaluate GitBook and its free tier capabilities
- Set up a task board system (possibly through wiki)
- Set up Cloudflare Pages CI for website

**Domain & Branding:**
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)

**Networking & Mentorship:**
- Ask friend launching text-to-speech startup about market insights
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits

**Personal/Other:**
- Finalize mountain route; share elevation profile with Yan