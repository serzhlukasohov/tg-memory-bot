# Startup Context
_Last updated: 2025-01-24 10:30 UTC_

## What we're building
Plyn is a voice-to-text keyboard app targeting the Polish market, with support for multilingual dictation and real-time translation capabilities. The product features voice input with text transformation modes (short, formal, warm styles) and works across Polish, Russian, and potentially Ukrainian languages. The core value proposition is superior translation quality compared to Google Translate, combined with seamless voice dictation functionality integrated directly into the mobile keyboard interface.

The product is currently in closed TestFlight beta testing phase, with a public website deployed at plyn.click for pre-launch marketing.

## Current Status
**Development Phase:** Near launch-ready. Core voice dictation and translation features are implemented and being dogfooded by the team. Authentication system and response styles feature remain incomplete.

**Critical Blockers:**
- Two critical bugs identified: dictated text sometimes fails to insert, and companion app loses connection requiring manual restarts
- Text mode locale bug: language changes don't propagate to text transformations
- Authentication system not yet implemented

**Infrastructure & Operations:**
- Public website deployed to plyn.click domain
- Using gemini-2.5-flash model for voice processing
- Shared wiki repository for documentation, with bot-maintained local copy
- Git authentication issues blocking automated bot operations
- Documentation debt accumulating as features are added outside wiki

**Marketing Strategy:** On pause. Team is consulting experts before choosing between simple email collection vs. paid pre-orders. ASO/ASA identified as promising growth channel pending cost clarification.

**Team Mode:** Aggressive shipping mode, deprioritizing nice-to-have features (dashboard, full keyboard, advanced activation) to focus on core voice functionality. Strong awareness of competitive pressure and emphasis on speed to market.

## Key Decisions Made
1. **Critical bugs must be fixed before user acquisition** - bugs will cause permanent user loss
2. **Domain secured:** plyn.click as public deployment address (not plin.click)
3. **Pause email capture development** pending marketing strategy decision from expert consultation
4. **Deprioritize non-core features** - dashboard, full keyboard, advanced activation deferred post-launch
5. **Text mode locale issue classified as product/UX bug** requiring fix, not optional feature
6. **Not fixing white corner video bug** - video will be replaced anyway
7. **Use ASO/ASA as primary growth channel** pending cost structure validation
8. **Multilingual support fixed in system prompt** - now working correctly across languages
9. **Firebase selected for authentication** infrastructure
10. **Wiki-based task tracking adopted** over separate project management tools

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
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?

**Marketing & GTM:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- Is the current model the same one that was previously being used? (related to performance slowdown)

**Product & UX:**
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- When should proper user research be conducted for the feature?
- What does Sergey think about fixing the locale issue with text modes?

**Infrastructure & Process:**
- Can Firebase system prompts be updated with versioning/rollback support?
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?
- How should wiki documentation be kept in sync with new features being added to the repository?
- What name, vibe, and emoji should be assigned to Plyn Bot?

## Next Actions

**Critical Path (Blocking Launch):**
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system
- Implement response styles (warm, friendly, etc.) in the app
- Fix text mode locale bug (language changes not propagating to transformations)

**Marketing & GTM:**
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Schedule ASO/ASA mentor call with Yan
- Create product demo video
- Record real demo video on actual device showing the keyboard in action
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw

**Research & Analysis:**
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Find open analytics on typical user monthly usage patterns
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Ask friend launching text-to-speech startup about market insights

**Product & Technical:**
- Merge pending pull requests
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages
- Investigate if direct keyboard voice activation is possible
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Add serzh to TestFlight
- Find Polish native speaker to verify localization

**Infrastructure & Operations:**
- Push local commit d45d1bb from environment with GitHub access (domain correction)
- Configure GitHub authentication (SSH keys or personal access token) for Plyn Bot's workspace environment
- Set up Cloudflare Pages CI for website
- Decide on documentation strategy for keeping wiki in sync with new features

**Planning & Coordination:**
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Create schematic launch plan to review together in next call
- Finalize mountain route; share elevation profile with Yan
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits