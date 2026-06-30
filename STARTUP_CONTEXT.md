# Startup Context
_Last updated: 2025-01-28_

## What we're building

Plyn is a mobile-first AI voice keyboard targeting Polish, Ukrainian, and Belarusian language speakers in Poland. The product combines voice-to-text transcription with AI-powered text enhancement ("beautification") to help users communicate more effectively, particularly emigrants who may not be fully fluent in Polish. 

Key differentiators:
- Voice-first input with real-time dictation
- AI enhancement layer that improves message quality
- Multi-language support (Polish, Russian, Ukrainian, Belarusian)
- Superior translation quality compared to Google Translate
- Positioned against Grammarly (which only added Polish in March 2026) but differentiated by voice input

The product is cloud-based using Gemini 2.5 Flash for speed-to-market, targeting non-technical users who value convenience over on-device privacy.

## Current Status

**Phase:** Pre-launch validation and final app development

**Infrastructure:**
- Website deployed at plyn.click (live)
- App in closed TestFlight testing
- Core voice dictation + AI enhancement working
- Documentation corrections made locally (awaiting git push due to auth issues)

**Immediate priorities:**
1. Fix git authentication for automated deployments
2. Implement response styles feature (last major feature before launch)
3. Create product demo video
4. Execute ASO/ASA marketing strategy (pending expert consultation)

**Known blockers:**
- Git push authentication issues in sandbox environment
- Critical bugs previously identified (text insertion failures, companion app connection issues) - status unclear if resolved
- Marketing validation approach undecided (simple email capture vs. paid pre-orders)

## Key Decisions Made

1. **Market pivot to Polish-speaking niche** - Abandoned saturated English desktop market for underserved Polish/Ukrainian/Belarusian emigrants in Poland
2. **Voice-first positioning** - Differentiate from Grammarly through voice input + AI enhancement, not just text correction
3. **Cloud-first architecture** - Prioritized speed-to-market with Gemini 2.5 Flash over on-device privacy
4. **Belarusian language as viral hook** - No existing mobile keyboards support it, potential organic growth driver
5. **Lean validation approach** - Landing page testing before full product build
6. **Aggressive feature deprioritization** - Cut dashboard, full keyboard, advanced activation to ship faster
7. **Domain strategy** - Secured plyn.click as primary domain (€9.05 via Cloudflare for plinklink.com as placeholder)
8. **Pause email capture** - Waiting for marketing expert consultation before choosing validation approach
9. **ASO/ASA as primary growth channel** - Identified as promising based on ~$200/geo economics
10. **Fix-before-launch discipline** - Explicit decision that critical bugs must be resolved before user acquisition to prevent churn

## Open Questions

**Market & Competition:**
- What is Grammarly's penetration in the Polish market and are they actively targeting it with ads?
- Is there any blocker preventing competitors from entering the Polish market?
- Do existing voice-to-text solutions actually target Polish, Ukrainian, and Russian markets?
- Can we find an underserved niche or use case for emigrants who don't know the local language?

**Pricing & Unit Economics:**
- What is the average price point Polish/Ukrainian/Belarusian users in Poland pay for similar subscription products?
- How many minutes of conversation fit into €5 budget based on actual token consumption?
- Does Gemini count 100 tokens per minute or 30 tokens per minute for audio?
- Are system prompt input tokens properly accounted for in cost calculations?
- What usage limits do competitors have on their subscription plans?
- Is there open analytics data on how many minutes users need per month?

**Marketing & Distribution:**
- Where and how to buy traffic to target the audience - Instagram, Facebook, TikTok, or other channels?
- Should pricing be displayed on the waitlist landing page?
- What does 'geo' mean in ASO/ASA pricing (~$200/geo) - is it per country or more granular?
- Should we do simple email list (weak validation) or paid pre-orders (strong validation but complex)?

**Technical:**
- Which AI model performs best for Polish language - likely Google/Gemini?
- Which models (Whisper v3, Gemini) work well with Polish and other target languages?
- Is it technically possible to access conversation context from within a custom keyboard on mobile?
- Can on-device models like Gemini's local version work effectively for non-English languages?
- Why does the language detection/switching work inconsistently - sometimes auto-translating, sometimes not?
- Is the current model the same one that was previously being used?
- Can I update the system prompt in Firebase, and is there versioning/rollback support?
- Is there actual latency delay when changing styles after dictation?
- Is it technically feasible to implement direct voice activation from keyboard?
- How does session termination work when keyboard goes to background?
- How does Whisper Flow handle incoming calls during sessions?
- How should GitHub authentication be configured for Plyn Bot's execution environment to enable push operations?

**Product & Content:**
- How to properly record demo video - with hands or just screencast?
- How popular are voice messages in different messengers and what's the demand for voice-to-text conversion?
- Can GitBook's free tier support the team's requirements?
- What name, vibe, and emoji should be assigned to Plyn Bot?
- Can Plyn Bot read and respond to messages in Cyrillic/non-English languages?

## Next Actions

**Critical Path (Launch Blockers):**
- Implement response styles feature (last major feature)
- Create product demo video
- Schedule ASO/ASA mentor call with Yan
- Resolve marketing validation approach decision
- Fix git authentication for automated deployments
- Push local commit d45d1bb from environment with GitHub access

**Marketing Preparation:**
- Research Grammarly's penetration and advertising activity in Polish market
- Manually verify Google search results for Polish keyboard-related queries
- Generate 3-5 killer feature ideas for emigrants who don't speak Polish well
- Research pricing - what Polish/Ukrainian/Belarusian users pay for subscriptions
- Build financial model and unit economics
- Research where to find target audience (Telegram expat groups, Facebook groups in Warsaw/Wroclaw)
- Set up email collection worker for landing page waitlist
- Set up Cloudflare Pages CI for website deployment
- Buy plyn.pl domain through GoDaddy broker (~$70)

**Product & Technical:**
- Test translation feature with Belarusian and Russian languages
- Find Polish native speaker to verify localization
- Test which AI model performs best for Polish language generation
- Watch JTBD video tutorial
- Perform competitor analysis (Wispr Flow, VoiceInk) - features, pricing, marketing
- Calculate cost per hour of text based on token usage
- Find open analytics on typical user monthly usage patterns
- Research which voice-to-text competitors support Polish/Ukrainian/Russian
- Test Whisper v3 and Gemini model performance with target languages
- Investigate conversation context access from custom keyboard
- Analyze voice message usage patterns in WhatsApp, Telegram
- Evaluate on-device models for non-English languages
- Evaluate GitBook free tier capabilities
- Test haptic vibration feedback on actual device
- Investigate direct keyboard voice activation feasibility
- Check how Whisper Flow handles session management
- Configure GitHub authentication (SSH keys or PAT) for Plyn Bot workspace

**Project Management:**
- Schedule sync call for timeline/roadmap (2-3 week sprint)
- Set up task board system (possibly through wiki)
- Finalize mountain route; share elevation profile with Yan
- Ask friend launching text-to-speech startup about market insights