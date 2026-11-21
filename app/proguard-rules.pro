# BFB.AI Shield - ProGuard Rules
-keepclassmembers class * extends android.service.quicksettings.TileService { public <methods>; }
-keep class com.shield.app.data.theme.** { *; }
-keep class com.shield.app.data.theme.ThemeDto { *; }
-dontwarn org.bouncycastle.**
