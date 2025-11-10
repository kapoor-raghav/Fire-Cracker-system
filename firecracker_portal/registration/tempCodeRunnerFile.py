
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Fresh')

# PDF upload field
    document = models.FileField(upload_to='documents/', blank=True, null=True)