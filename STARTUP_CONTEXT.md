# Startup Context
_Last updated: 2024-12-20 14:30 UTC_

## What we're building
Plyn is a voice-first AI keyboard for mobile targeting Polish, Ukrainian, Russian, and Belarusian language speakers in Poland. The product combines real-time voice transcription with AI beautification and translation capabilities, differentiating from competitors like Grammarly through voice-first input and multi-language support for emigrant communities. Currently deployed at plyn.click, the app is in closed TestFlight beta and approaching public launch. Unit economics show €5/month can support ~4 hours of usage using Gemini API for audio and text processing.

## Current Status
**Launch-ready phase with strategic pause on marketing validation.** The website is live at plyn.click with domain correctly configured. App development is nearly complete - only response styles feature remains before technical launch readiness. The team is deliberately consulting experts before choosing between simple email collection versus complex paid pre-orders for market validation. ASO/ASA has emerged as a promising growth channel pending cost structure clarity (~$200/geo). Critical bugs (text insertion failures, companion app connection issues) have been identified and must be fixed before user acquisition begins.

## Key Decisions Made
- **2024-12**: Pivot from English desktop voice-to-text to Polish/Ukrainian/Russian/Belarusian mobile keyboard serving emigrants in Poland
- **2024-12**: Target Grammarly's market gap (only added Polish March 2026) with voice-first differentiation
- **2024-12**: Belarusian language support as viral GTM hook (no mobile keyboards currently support it)
- **2024-12**: Lean validation approach with landing page before full product build (compressed to 2-3 week timeline)
- **2024-12**: Cloud-based MVP over privacy-focused on-device processing for speed to market
- **2024-12**: Aggressive shipping mode - deprioritize dashboard, full keyboard, advanced activation to focus on core voice input
- **2024-12**: Critical bugs must be fixed before user acquisition (retention risk)
- **2024-12**: Website deployed to plyn.click as public domain (corrected from plin.click typo)
- **2024-12**: Pause email capture feature pending marketing strategy expert consultation
- **2024-12**: All wiki documentation corrected to reflect proper plyn.click domain

## Open Questions
**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?

**Pricing & Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Marketing & Go-to-Market:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?
- How to properly record demo video - with hands or just screencast?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Product:**
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- When should proper user research be conducted for the feature?

**Operations:**
- Can GitBook's free tier support the team's requirements?
- Should we set up a task board through wiki or another tool?
- What name, vibe, and emoji should be assigned to Plyn Bot?
- Did the git push succeed after settings changes?

## Next Actions

**Critical Path (Launch Blockers):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement response styles (warm, friendly, etc.) in the app
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy

**Marketing & Validation:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Create product demo video
- Schedule ASO/ASA mentor call with Yan
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Set up email collection worker for landing page waitlist (paused pending strategy decision)

**Product Development:**
- Test which AI model performs best for Polish language generation
- Find Polish native speaker to verify localization
- Merge the pending pull requests
- Test the updated system prompt across all languages
- Investigate if direct keyboard voice activation is possible

**Research & Analysis:**
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Business Planning:**
- Build financial model and unit economics for the business
- Create schematic launch plan to review together in next call
- Review competitor subscription limits and pricing tiers
- Schedule sync call to create timeline and roadmap

**Infrastructure & Operations:**
- Execute git push after settings modification
- Set up Cloudflare Pages CI for website
- Evaluate GitBook and its free tier capabilities
- Set up a task board system (possibly through wiki)
- Provide bot configuration (name/vibe/emoji) or review suggested options

**Lower Priority:**
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits
- Ask friend launching text-to-speech startup about market insights
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Check how Whisper Flow handles session management and keyboard background behavior
- Replace the video on the website
- Finalize mountain route; share elevation profile with Yan