# Instructions to Create GitHub Repositories

## Quick Steps

1. **Go to GitHub**: https://github.com/new

2. **Create each repository** (one at a time):
   - Repository name: `patient-service`
   - Description: "Patient Service - Microservice for managing patient information"
   - Visibility: Public or Private (your choice)
   - **IMPORTANT**: Do NOT check "Add a README file", "Add .gitignore", or "Choose a license"
   - Click "Create repository"

3. **Repeat for all 7 services**:
   - `patient-service`
   - `doctor-service`
   - `billing-service`
   - `appointment-service`
   - `prescription-service`
   - `payment-service`
   - `notification-service`

## After Creating All Repositories

Run this command to push all services:

```powershell
.\push-after-repos-created.ps1
```

Or push each one manually:

```powershell
cd patient-service
git push -u origin main
cd ..

cd doctor-service
git push -u origin main
cd ..

# ... and so on for each service
```

## Quick Create Script (Alternative)

If you want to create them faster, you can:

1. Open https://github.com/new in your browser
2. Create the first repo (`patient-service`)
3. After creating, the URL will be: `https://github.com/vamsigorle29/patient-service`
4. Change the repo name in the URL to create the next one:
   - `https://github.com/vamsigorle29/doctor-service` (just change the name)
   - But you'll still need to click through the creation process

## Verification

After pushing, verify each repository:
- https://github.com/vamsigorle29/patient-service
- https://github.com/vamsigorle29/doctor-service
- https://github.com/vamsigorle29/billing-service
- https://github.com/vamsigorle29/appointment-service
- https://github.com/vamsigorle29/prescription-service
- https://github.com/vamsigorle29/payment-service
- https://github.com/vamsigorle29/notification-service

