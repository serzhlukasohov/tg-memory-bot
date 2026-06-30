# Startup Context
_Last updated: 2025-01-26 14:30 UTC_

## What we're building

Plyn is a Polish voice-to-text keyboard app with real-time multilingual dictation and translation capabilities. The product supports Polish, Russian, and other languages, with voice input that can auto-translate between languages. The app includes text transformation modes (short, formal, warm styles) and is positioned as a solution for emigrants and Polish market users who need superior voice-to-text quality compared to Google's machine translation.

The product uses Gemini 2.5 Flash model for processing and is currently in closed TestFlight beta with invitation-controlled access. Public website deployed at plyn.click.

## Current Status

**Phase**: Pre-launch - aggressive shipping mode focused on core functionality

**Immediate Priorities**:
- Critical bug fixes blocking user acquisition (text insertion failures, companion app connection drops)
- Response styles implementation (last feature before launch readiness)
- Marketing validation and ASO/ASA strategy decision
- Product demo video creation
- Recent UX bug identified: text mode doesn't respect locale changes (preserves original language instead of current locale)

**Recent Milestones**:
- Website deployed to plyn.click domain
- Text mode with multiple styles shipped by Sergey
- Translation functionality fixed and working well
- UI polish completed (haptic/audio feedback)
- Multilingual support fixed in system prompt
- Team actively dogfooding the product

**Blockers**:
- Authentication system not implemented (Firebase access granted but not configured)
- Critical stability bugs preventing proper user research
- Git/SSH authentication issues blocking Plyn Bot automation
- Documentation debt growing as features ship outside wiki
- Marketing strategy decision needed before email capture development

## Key Decisions Made

1. **Critical bugs must be fixed before user acquisition** - users who encounter bugs will leave permanently
2. **Domain acquired**: plyn.click as public deployment address (corrected from initial plin.click)
3. **Aggressive feature deprioritization** - consciously cutting dashboard, full keyboard, advanced activation to focus on core voice input
4. **Pause email capture development** - pending marketing strategy consultation with experts
5. **Text mode locale issue classified as product/UX bug** - not a feature, needs fixing
6. **Speed to market over feature completeness** - aware of competitive pressure, prioritizing launch velocity
7. **Not fixing website video white corners bug** - video will be replaced anyway
8. **Evaluating competitors selectively** - studying UX patterns but being deliberate about what to implement now vs later
9. **Placeholder domain acquired**: plinklink.com via Cloudflare for €9.05
10. **Moving to structured task tracking** - recognizing project management gaps, implementing board system

## Open Questions

**Market & Competition**:
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Can we find an underserved niche or use case (e.g., emigrants who don't know the local language)?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?

**Pricing & Economics**:
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Marketing & GTM**:
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?

**Technical**:
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Can GitBook's free tier support the team's requirements?
- How should authentication be implemented?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Infrastructure**:
- Can I update the system prompt in Firebase, and is there versioning/rollback support?
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?
- How to configure SSH key access for the bot's execution environment to authenticate with GitHub?

**Product/UX**:
- When should proper user research be conducted for the feature?
- Should we set up a task board through wiki or another tool?

## Next Actions

**Critical Path (Blocking Launch)**:
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Implement authentication system
- Implement response styles (warm, friendly, etc.) in the app
- Fix text mode locale bug (language not respecting user's current locale selection)

**Marketing & Validation**:
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Schedule ASO/ASA mentor call with Yan
- Create product demo video
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products

**Market Research**:
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Build financial model and unit economics for the business
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers

**Technical Tasks**:
- Merge the pending pull requests
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages
- Investigate if direct keyboard voice activation is possible
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Evaluate GitBook and its free tier capabilities
- Check how Whisper Flow handles session management and keyboard background behavior

**Infrastructure & Deployment**:
- Set up Cloudflare Pages CI for website
- Push local commit d45d1bb from environment with GitHub access (domain corrections)
- Configure GitHub authentication (SSH keys or personal access token) for Plyn Bot's workspace environment
- Fix SSH key configuration for Plyn Bot's workspace environment to enable GitHub repository access

**Team & Process**:
- Set up a task board system (possibly through wiki)
- Find Polish native speaker to verify localization
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Set up shared AI agent with knowledge base in chat to track all decisions and research
- Watch JTBD (Jobs-to-be-Done) website tutorial when time permits
- Ask friend launching text-to-speech startup about market insights
- Finalize mountain route; share elevation profile with Yan

**Deferred/Lower Priority**:
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Replace the video on the website
- Complete landing page design and development on plyn-site.vercel.app
- Set up email collection worker for landing page waitlist (paused pending marketing strategy)