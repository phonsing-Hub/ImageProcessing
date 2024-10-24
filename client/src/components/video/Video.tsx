import HeroVideoDialog from "@/components/ui/hero-video-dialog";
function Video() {
  return (
    <div className="relative">
    <HeroVideoDialog
      className="dark:hidden block"
      animationStyle="from-bottom"
      videoSrc="http://localhost:8000/video"
      thumbnailSrc="https://startup-template-sage.vercel.app/hero-light.png"
      thumbnailAlt="Hero Video"
    />
  </div>
  )
}

export default Video