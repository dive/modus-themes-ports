(require 'json)

(defun modus-themes--theme-name-from-file (file)
  (let ((base (file-name-base file)))
    (if (string-suffix-p "-theme" base)
        (substring base 0 (- (length base) (length "-theme")))
      base)))

(defun modus-themes--normalize-value (value)
  (cond
   ((stringp value) value)
   ((symbolp value) (symbol-name value))
   (t (format "%S" value))))

(defun modus-themes--entry-value (entry)
  (let ((raw (cdr entry)))
    (cond
     ((and (consp raw) (null (cdr raw))) (car raw))
     ((consp raw) (car raw))
     (t raw))))

(defun modus-themes--normalize-palette (palette)
  (let (items)
    (dolist (entry palette)
      (let ((key (car entry))
            (val (modus-themes--entry-value entry)))
        (when (symbolp key)
          (push (cons (symbol-name key) (modus-themes--normalize-value val)) items))))
    (sort items (lambda (a b) (string< (car a) (car b))))))

(defun modus-themes--write-json (obj path)
  (with-temp-buffer
    (insert (json-encode obj))
    (json-pretty-print-buffer)
    (write-region (point-min) (point-max) path nil 'silent)))

(defun modus-themes-export-palettes (themes-dir out-dir)
  (let* ((themes-dir (file-name-as-directory (expand-file-name themes-dir)))
         (out-dir (file-name-as-directory (expand-file-name out-dir))))
    (unless (file-directory-p themes-dir)
      (error "Themes directory not found: %s" themes-dir))
    (unless (file-directory-p out-dir)
      (make-directory out-dir t))

    (add-to-list 'load-path themes-dir)
    (require 'modus-themes)

    (let ((theme-files (directory-files themes-dir t "-theme\\.el$")))
      (when (null theme-files)
        (error "No theme files found in %s" themes-dir))
      (dolist (theme-file theme-files)
        (load-file theme-file)
        (let* ((theme-name (modus-themes--theme-name-from-file theme-file))
               (palette-var (intern (concat theme-name "-palette"))))
          (unless (boundp palette-var)
            (error "Palette variable not found: %s" palette-var))
          (let* ((palette (symbol-value palette-var))
                 (normalized (modus-themes--normalize-palette palette))
                 (obj `((name . ,theme-name)
                        (palette . ,normalized)))
                 (out-file (expand-file-name (concat theme-name ".json") out-dir)))
            (modus-themes--write-json obj out-file)))))))

(provide 'extract-palettes)
