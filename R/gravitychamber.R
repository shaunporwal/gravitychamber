# From here to make moving elf
# Need to do something similar to make gravity chamber with black pixels,
# and controllable gravity parameter

link_v_top <- c(
  0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,
  0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,
  0,0,2,0,1,3,3,3,3,3,3,1,0,2,0,0,
  0,0,2,0,3,3,3,3,3,3,3,3,0,2,0,0,

  0,0,2,2,3,2,1,2,2,1,2,3,2,2,0,0,
  0,0,2,2,3,2,3,2,2,3,2,3,2,2,0,0,
  0,0,0,2,2,2,2,2,2,2,2,2,2,3,0,0
)

link_v_b1 <- c(
  0,0,0,1,1,2,2,3,3,2,2,1,1,3,0,0,

  0,3,3,3,3,3,2,2,2,2,1,1,3,3,3,0,
  3,3,2,3,3,3,3,1,1,1,1,1,2,3,3,0,
  3,2,2,2,3,3,2,3,3,1,1,2,2,2,3,0,
  3,3,2,3,3,3,2,1,3,3,3,3,2,2,2,0,

  3,3,2,3,3,3,2,3,3,1,1,1,1,2,0,0,
  3,3,3,3,3,3,2,1,1,1,1,1,0,0,0,0,
  0,2,2,2,2,2,3,0,0,3,3,3,0,0,0,0,
  0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0
)

link_v_b2 <- c(
  0,0,0,0,1,2,2,3,3,2,2,1,3,3,0,0,

  0,0,3,3,3,3,3,2,2,2,1,1,1,2,0,0,
  0,3,3,2,3,3,3,3,1,1,1,1,1,2,0,0,
  0,3,2,2,2,3,3,2,3,3,1,1,3,0,0,0,
  0,3,3,2,3,3,3,2,1,3,3,3,1,0,0,0,

  0,3,3,2,3,3,3,2,3,3,1,1,1,0,0,0,
  0,3,3,3,3,3,3,2,1,1,1,3,0,0,0,0,
  0,0,2,2,2,2,2,0,0,3,3,3,0,0,0,0,
  0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,0
)

# Combine vectors to get frames
link_f1 <- c(link_v_top, link_v_b1)
link_f2 <- c(link_v_top, link_v_b2)


tmp <- tempdir()  # store temporary folder path

# Function to write frame to temporary folder
write_link <- function(vec) {
  write_path <- file.path(tmp, paste0(substitute(vec), ".png"))
  png(write_path, width = 160, height = 160)
  link_m <- matrix(vec, 16)
  link_m <- link_m[, ncol(link_m):1]
  par(mar = rep(0, 4))
  link_cols <- c("white", "#7bc702", "#cc8f2d", "#6c430a")
  image(link_m, col = link_cols)
  dev.off()
}

# Write the frames
write_link(link_f1); write_link(link_f2)



# Generate a gif from the saved frames
png_paths <- list.files(tmp, "*.png$", full.names = TRUE)     # get file paths
frames <- magick::image_read(png_paths)                       # load the files
magick::image_animate(frames, fps = 2, dispose = "previous")
