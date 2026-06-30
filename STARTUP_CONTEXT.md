# Startup Context
_Last updated: 2025-01-28 19:45 UTC_

## What we're building
Plyn is a voice-to-text keyboard app for iOS targeting the Polish market, with multilingual support for Polish, Ukrainian, Russian, and Belarusian languages. The product features real-time voice dictation with translation capabilities, text mode transformations (short, formal, warm styles), and is powered by Gemini AI models. The app is positioned to serve emigrants in Poland who need efficient multilingual communication tools. Public website deployed at plyn.click.

## Current Status
App development is 95% complete - core voice dictation and translation working well, UI polished with haptic/audio feedback. Currently in aggressive shipping mode, deprioritizing nice-to-have features to focus on launch. Critical blockers resolved, now implementing final feature (response styles). Website live at plyn.click. Moving into financial planning phase to establish unit economics and pricing model. Team encountering infrastructure limitations (gog tool for Google Sheets not installed, git authentication issues for bot). Authentication system still pending implementation. Marketing strategy paused pending expert consultation on email capture vs paid pre-orders approach.

## Key Decisions Made
1. **Domain acquisition** - Secured plyn.click as public deployment domain (plinklink.com acquired as placeholder)
2. **Aggressive shipping mode** - Deprioritized dashboard, full keyboard, and advanced activation features to focus on core voice input
3. **Marketing pause** - Deliberately pausing email capture development pending expert consultation on validation strategy
4. **Financial tooling** - Google Sheets as source of truth for financial models, with markdown/CSV interim format until gog tool available
5. **Bug prioritization** - Fixed critical insertion and connection bugs before user acquisition; deprioritized minor desktop video transition bug
6. **Multilingual positioning** - Targeting Polish market with Polish/Ukrainian/Russian/Belarusian support for emigrant users
7. **Task management** - Moving from conversational tracking to structured wiki-based task board system
8. **Documentation strategy** - Plyn Bot maintains local wiki copy; English for documentation, Russian for team communication
9. **Text mode locale handling** - Classified as UX bug (locale changes don't propagate to transformations)
10. **Growth channel focus** - ASO/ASA model identified as promising, pending cost structure clarity

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

**Pricing & Unit Economics:**
- Should pricing be displayed on the waitlist landing page?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Why does the language detection/switching work inconsistently - sometimes auto-translating, sometimes not?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Infrastructure & Process:**
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?
- Is Google OAuth configured in the environment to enable Plyn Bot to work with Google Sheets?
- How should wiki documentation be kept in sync with new features being added to the repository?
- Can topics be added to a Telegram group after it has been created?

**Content & Marketing:**
- How to properly record demo video - with hands or just screencast?
- What name, vibe, and emoji should be assigned to Plyn Bot?

## Next Actions

**Critical Path (Launch Blockers):**
- Implement response styles (warm, friendly, etc.) in the app
- Implement authentication system
- Create product demo video
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy

**Financial Planning:**
- Build financial model and unit economics for the business
- Create financial model structure in MD/CSV format in repository (assumptions, pricing, usage, costs, scenarios, formulas)
- Create financial model and unit economics calculations in Google Sheets with wiki summary (once gog available)
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Market Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Ask friend launching text-to-speech startup about market insights

**Marketing & Growth:**
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Set up email collection worker for landing page waitlist (paused pending strategy decision)
- Schedule ASO/ASA mentor call with Yan

**Technical Testing:**
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages

**Technical Investigation:**
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Investigate if direct keyboard voice activation is possible
- Check how Whisper Flow handles session management and keyboard background behavior

**Bug Fixes:**
- Fix text mode locale bug (locale changes don't propagate to transformations)
- Review and respond to the text mode locale bug classification

**Infrastructure:**
- Configure GitHub authentication (SSH keys or personal access token) for Plyn Bot's workspace environment
- Push local commit d45d1bb from environment with GitHub access
- Grant admin access to Yanka for the group

**Documentation & Process:**
- Find Polish native speaker to verify localization
- Update wiki documentation to reflect new features being added
- Decide on documentation strategy for keeping wiki in sync with new features

**Planning:**
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Create schematic launch plan to review together in next call
- Finalize mountain route; share elevation profile with Yan

**Learning:**
- Watch JTBD (Jobs-to-be-Done) video tutorial when time permits