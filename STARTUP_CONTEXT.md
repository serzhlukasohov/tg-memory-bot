# Startup Context
_Last updated: 2025-01-21_

## What we're building

Plyn is a voice-to-text keyboard app targeting Polish-speaking users (including Ukrainian and Belarusian emigrants in Poland). The product features real-time voice dictation with translation capabilities across Polish, Russian, and multiple languages, using Gemini 2.5 Flash for superior translation quality compared to Google Translate. The app includes text mode transformations with multiple styles (short, formal, warm), haptic and audio feedback, and a companion app architecture. The product is positioned for the Polish market where competitors like Grammarly and other voice-to-text solutions have minimal presence.

## Current Status

**Launch readiness:** App development is nearly complete with only response styles remaining before technical launch readiness. Website is deployed at plyn.click with domain secured.

**Strategic pause:** Team is deliberately consulting experts before finalizing go-to-market strategy, specifically around marketing validation approach (email collection vs. paid pre-orders) and ASO/ASA channel economics.

**Active focus areas:**
- Financial modeling and unit economics planning (moving to Google Sheets infrastructure)
- Marketing strategy validation before launch
- Product polish (response styles, UX bugs)

**Known critical issues:**
- Text mode locale bug: language changes don't propagate to transformations
- Documentation debt: new features added outside wiki system
- Plyn Bot git authentication blocked (SSH key configuration needed)

## Key Decisions Made

1. **Aggressive shipping mode** - Deprioritizing dashboard, full keyboard, advanced activation to focus on core voice input functionality
2. **Google Sheets for financial modeling** - Established as source of truth for unit economics with wiki summaries for documentation
3. **Domain strategy** - plyn.click as public deployment domain (corrected from initial plin.click)
4. **Marketing validation pause** - Consulting experts before choosing between simple email collection vs. complex paid pre-orders
5. **ASO/ASA as primary growth channel** - Identified as promising model pending cost structure clarity
6. **Not fixing desktop video transition bug** - White corners issue deprioritized since video content will be replaced
7. **Firebase for system prompt management** - Granted access; versioning questions remain open
8. **Gemini 2.5 Flash as primary model** - Despite performance concerns, superior translation quality vs. competitors
9. **Task tracking via wiki board** - Moving from conversation-based to structured task management
10. **Text mode locale issue classified as bug** - Not a feature; needs fixing for proper UX

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

**Marketing & Launch:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- How to properly record demo video - with hands or just screencast?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Why does the language detection/switching work inconsistently - sometimes auto-translating, sometimes not?
- Is the current model the same one that was previously being used?
- Why is the system running slowly?
- Can I update the system prompt in Firebase, and is there versioning/rollback support?
- How should authentication be implemented?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?

**Product & UX:**
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- When should proper user research be conducted for the feature?
- What does Sergey think about fixing the locale issue with text modes?

**Infrastructure & Process:**
- Can GitBook's free tier support the team's requirements?
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?
- How should wiki documentation be kept in sync with new features being added to the repository?

## Next Actions

**Marketing & Research:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries to confirm lack of competition
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research pricing - what Polish/Ukrainian/Belarusian users in Poland typically pay for subscription products
- Research where to find and how to engage target audience - Telegram expat groups, Facebook groups in Warsaw/Wroclaw
- Schedule call with marketing contact to discuss ASO/ASA model and pre-order strategy
- Schedule ASO/ASA mentor call with Yan
- Perform competitor analysis of Wispr Flow, VoiceInk, and others - analyze value propositions, features, marketing, and pricing plans
- Review competitor subscription limits and pricing tiers
- Research which voice-to-text competitors actually support and target Polish, Ukrainian, Russian markets
- Analyze voice message usage patterns and demand for transcription in WhatsApp, Telegram, and other messengers
- Ask friend launching text-to-speech startup about market insights

**Financial Modeling:**
- Build financial model and unit economics for the business
- Calculate cost per hour of text based on token usage, verify token counting methodology
- Find open analytics on typical user monthly usage patterns

**Product Development:**
- Implement response styles (warm, friendly, etc.) in the app
- Review and respond to the text mode locale bug classification
- Fix critical bug where dictated text doesn't insert
- Fix companion app connection issue requiring restart (red light indicator)
- Debug the system prompt to understand and fix inconsistent language detection behavior
- Update system prompt in Firebase
- Implement authentication system
- Test haptic vibration feedback on actual device
- Review sound and haptic feedback implementation
- Test the updated system prompt across all languages
- Investigate if direct keyboard voice activation is possible
- Merge the pending pull requests
- Check how Whisper Flow handles session management and keyboard background behavior
- Test which AI model performs best for Polish language generation
- Test Whisper v3 and Gemini model performance with Polish and other target languages
- Investigate technical feasibility of accessing conversation context from custom mobile keyboard
- Evaluate GitBook and its free tier capabilities

**Launch Preparation:**
- Complete landing page design and development on plyn-site.vercel.app
- Record real demo video on actual device showing the keyboard in action
- Create product demo video
- Set up email collection worker for landing page waitlist (paused pending marketing strategy decision)
- Buy domain - research plyn.pl acquisition through GoDaddy broker (~$70)
- Find Polish native speaker to verify localization
- Create schematic launch plan to review together in next call
- Set up Cloudflare Pages CI for website; deploy to plink.link
- Add serzh to TestFlight
- Rebuild/redraw the APK after adding Polish language

**Infrastructure & Process:**
- Configure GitHub authentication (SSH keys or personal access token) for Plyn Bot's workspace environment
- Fix SSH key configuration for Plyn Bot's workspace environment to enable GitHub repository access
- Push local commit d45d1bb from environment with GitHub access
- Decide on documentation strategy for keeping wiki in sync with new features
- Set up a task board system (possibly through wiki)
- Set up shared AI agent with knowledge base in chat to track all decisions and research

**Planning & Coordination:**
- Schedule sync call to create timeline and roadmap - aim for 2-3 week sprint to landing page launch
- Finalize