import * as z from "zod";

export const resetPasswordSchema = z
  .object({
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password !== data.confirmPassword, {
    message: "Password do not match",
    path: ["confirmPassword"],
  });

export type resetPasswordFormValues = z.infer<typeof resetPasswordSchema>;
